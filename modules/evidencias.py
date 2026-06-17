import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one

def mostrar_evidencias():
    st.subheader("📂 Gestión de Evidencias")

    cursos = fetch_all(
        """
        SELECT id_curso, nombre_curso, ciclo, seccion
        FROM cursos
        ORDER BY nombre_curso
        """
    )

    if not cursos:
        st.warning("Primero debes registrar al menos un curso.")
        return

    opciones_cursos = {
        f"{curso['nombre_curso']} | Ciclo {curso['ciclo']} | Sección {curso['seccion']}": curso["id_curso"]
        for curso in cursos
    }

    # =========================
    # REGISTRAR EVIDENCIA
    # =========================
    st.markdown("### Registrar evidencia")

    curso_label = st.selectbox("Curso", list(opciones_cursos.keys()), key="curso_evidencia_nuevo")
    id_curso = opciones_cursos[curso_label]

    estudiantes = fetch_all(
        """
        SELECT id_estudiante, nombres, apellidos
        FROM estudiantes
        WHERE id_curso = ?
        ORDER BY apellidos, nombres
        """,
        (id_curso,)
    )

    if not estudiantes:
        st.warning("Ese curso aún no tiene estudiantes registrados.")
        return

    criterios = fetch_all(
        """
        SELECT id_criterio, criterio
        FROM criterios_evaluacion
        WHERE id_curso = ?
        ORDER BY id_criterio DESC
        """,
        (id_curso,)
    )

    if not criterios:
        st.warning("Ese curso aún no tiene criterios registrados.")
        return

    rubricas = fetch_all(
        """
        SELECT id_rubrica, nombre_rubrica
        FROM rubricas
        WHERE id_curso = ?
        ORDER BY id_rubrica DESC
        """,
        (id_curso,)
    )

    opciones_estudiantes = {
        f"{estudiante['apellidos']}, {estudiante['nombres']}": estudiante["id_estudiante"]
        for estudiante in estudiantes
    }

    opciones_criterios = {
        criterio["criterio"]: criterio["id_criterio"]
        for criterio in criterios
    }

    opciones_rubricas = {
        rubrica["nombre_rubrica"]: rubrica["id_rubrica"]
        for rubrica in rubricas
    }

    with st.form("form_evidencia"):
        estudiante_label = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        criterio_label = st.selectbox("Criterio de evaluación", list(opciones_criterios.keys()))

        if opciones_rubricas:
            rubrica_label = st.selectbox("Rúbrica asociada", list(opciones_rubricas.keys()))
            id_rubrica = opciones_rubricas[rubrica_label]
        else:
            st.info("Este curso aún no tiene rúbricas registradas.")
            id_rubrica = None

        tipo_evidencia = st.selectbox(
            "Tipo de evidencia",
            [
                "Trabajo escrito",
                "Exposición",
                "Sesión de aprendizaje",
                "Portafolio",
                "Microenseñanza",
                "Práctica pedagógica",
                "Video",
                "Otro"
            ]
        )

        nombre_evidencia = st.text_input("Nombre de la evidencia")
        descripcion = st.text_area("Descripción")
        fecha_entrega = st.date_input("Fecha de entrega")
        estado_entrega = st.selectbox(
            "Estado de entrega",
            ["Entregado", "Pendiente", "En revisión"]
        )

        submitted = st.form_submit_button("Guardar evidencia")

    if submitted:
        id_estudiante = opciones_estudiantes[estudiante_label]
        id_criterio = opciones_criterios[criterio_label]

        if not nombre_evidencia.strip():
            st.error("El nombre de la evidencia es obligatorio.")
        else:
            execute_query(
                """
                INSERT INTO evidencias (
                    id_estudiante,
                    id_curso,
                    id_criterio,
                    id_rubrica,
                    tipo_evidencia,
                    nombre_evidencia,
                    descripcion,
                    fecha_entrega,
                    estado_entrega
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    id_estudiante,
                    id_curso,
                    id_criterio,
                    id_rubrica,
                    tipo_evidencia,
                    nombre_evidencia,
                    descripcion,
                    str(fecha_entrega),
                    estado_entrega
                )
            )
            st.success("Evidencia registrada correctamente.")

    # =========================
    # LISTA DE EVIDENCIAS
    # =========================
    st.markdown("### Lista de evidencias")

    evidencias = fetch_all(
        """
        SELECT
            e.id_evidencia,
            e.id_estudiante,
            e.id_curso,
            e.id_criterio,
            e.id_rubrica,
            es.apellidos || ', ' || es.nombres AS estudiante,
            c.nombre_curso,
            ce.criterio,
            e.tipo_evidencia,
            e.nombre_evidencia,
            e.descripcion,
            e.fecha_entrega,
            e.estado_entrega
        FROM evidencias e
        INNER JOIN estudiantes es ON e.id_estudiante = es.id_estudiante
        INNER JOIN cursos c ON e.id_curso = c.id_curso
        INNER JOIN criterios_evaluacion ce ON e.id_criterio = ce.id_criterio
        ORDER BY e.id_evidencia DESC
        """
    )

    if evidencias:
        df = pd.DataFrame([dict(row) for row in evidencias])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay evidencias registradas.")
        return

    # =========================
    # EDITAR EVIDENCIA
    # =========================
    st.markdown("### Editar evidencia")

    opciones_evidencias = {
        f"{evidencia['id_evidencia']} - {evidencia['nombre_evidencia']} ({evidencia['estudiante']})": evidencia["id_evidencia"]
        for evidencia in evidencias
    }

    evidencia_editar_label = st.selectbox(
        "Selecciona la evidencia a editar",
        list(opciones_evidencias.keys()),
        key="evidencia_editar_select"
    )

    id_evidencia_editar = opciones_evidencias[evidencia_editar_label]

    evidencia_actual = fetch_one(
        """
        SELECT *
        FROM evidencias
        WHERE id_evidencia = ?
        """,
        (id_evidencia_editar,)
    )

    curso_actual_id = evidencia_actual["id_curso"] if evidencia_actual else None
    labels_cursos = list(opciones_cursos.keys())
    index_curso_actual = 0

    for i, label in enumerate(labels_cursos):
        if opciones_cursos[label] == curso_actual_id:
            index_curso_actual = i
            break

    curso_editar_label = st.selectbox(
        "Curso de la evidencia",
        labels_cursos,
        index=index_curso_actual,
        key="evidencia_curso_editar"
    )

    id_curso_editar = opciones_cursos[curso_editar_label]

    estudiantes_editar = fetch_all(
        """
        SELECT id_estudiante, nombres, apellidos
        FROM estudiantes
        WHERE id_curso = ?
        ORDER BY apellidos, nombres
        """,
        (id_curso_editar,)
    )

    criterios_editar = fetch_all(
        """
        SELECT id_criterio, criterio
        FROM criterios_evaluacion
        WHERE id_curso = ?
        ORDER BY id_criterio DESC
        """,
        (id_curso_editar,)
    )

    rubricas_editar = fetch_all(
        """
        SELECT id_rubrica, nombre_rubrica
        FROM rubricas
        WHERE id_curso = ?
        ORDER BY id_rubrica DESC
        """,
        (id_curso_editar,)
    )

    opciones_estudiantes_editar = {
        f"{estudiante['apellidos']}, {estudiante['nombres']}": estudiante["id_estudiante"]
        for estudiante in estudiantes_editar
    }

    opciones_criterios_editar = {
        criterio["criterio"]: criterio["id_criterio"]
        for criterio in criterios_editar
    }

    opciones_rubricas_editar = {
        rubrica["nombre_rubrica"]: rubrica["id_rubrica"]
        for rubrica in rubricas_editar
    }

    labels_estudiantes = list(opciones_estudiantes_editar.keys())
    index_estudiante_actual = 0
    for i, label in enumerate(labels_estudiantes):
        if opciones_estudiantes_editar[label] == evidencia_actual["id_estudiante"]:
            index_estudiante_actual = i
            break

    labels_criterios = list(opciones_criterios_editar.keys())
    index_criterio_actual = 0
    for i, label in enumerate(labels_criterios):
        if opciones_criterios_editar[label] == evidencia_actual["id_criterio"]:
            index_criterio_actual = i
            break

    labels_rubricas = list(opciones_rubricas_editar.keys())
    index_rubrica_actual = 0
    if evidencia_actual["id_rubrica"] is not None and labels_rubricas:
        for i, label in enumerate(labels_rubricas):
            if opciones_rubricas_editar[label] == evidencia_actual["id_rubrica"]:
                index_rubrica_actual = i
                break

    tipos_evidencia = [
        "Trabajo escrito",
        "Exposición",
        "Sesión de aprendizaje",
        "Portafolio",
        "Microenseñanza",
        "Práctica pedagógica",
        "Video",
        "Otro"
    ]

    estados_entrega = ["Entregado", "Pendiente", "En revisión"]

    with st.form("form_editar_evidencia"):
        editar_estudiante_label = st.selectbox(
            "Estudiante",
            labels_estudiantes,
            index=index_estudiante_actual
        )

        editar_criterio_label = st.selectbox(
            "Criterio de evaluación",
            labels_criterios,
            index=index_criterio_actual
        )

        if labels_rubricas:
            editar_rubrica_label = st.selectbox(
                "Rúbrica asociada",
                labels_rubricas,
                index=index_rubrica_actual
            )
        else:
            st.info("Este curso no tiene rúbricas registradas.")
            editar_rubrica_label = None

        editar_tipo_evidencia = st.selectbox(
            "Tipo de evidencia",
            tipos_evidencia,
            index=tipos_evidencia.index(evidencia_actual["tipo_evidencia"]) if evidencia_actual["tipo_evidencia"] in tipos_evidencia else 0
        )

        editar_nombre_evidencia = st.text_input(
            "Nombre de la evidencia",
            value=evidencia_actual["nombre_evidencia"] if evidencia_actual else ""
        )

        editar_descripcion = st.text_area(
            "Descripción",
            value=evidencia_actual["descripcion"] if evidencia_actual and evidencia_actual["descripcion"] else ""
        )

        editar_fecha_entrega = st.text_input(
            "Fecha de entrega (YYYY-MM-DD)",
            value=evidencia_actual["fecha_entrega"] if evidencia_actual and evidencia_actual["fecha_entrega"] else ""
        )

        editar_estado_entrega = st.selectbox(
            "Estado de entrega",
            estados_entrega,
            index=estados_entrega.index(evidencia_actual["estado_entrega"]) if evidencia_actual["estado_entrega"] in estados_entrega else 0
        )

        submitted_editar = st.form_submit_button("Actualizar evidencia")

    if submitted_editar:
        id_estudiante_nuevo = opciones_estudiantes_editar[editar_estudiante_label]
        id_criterio_nuevo = opciones_criterios_editar[editar_criterio_label]
        id_rubrica_nueva = opciones_rubricas_editar[editar_rubrica_label] if editar_rubrica_label else None

        if not editar_nombre_evidencia.strip():
            st.error("El nombre de la evidencia es obligatorio.")
        else:
            execute_query(
                """
                UPDATE evidencias
                SET id_estudiante = ?,
                    id_curso = ?,
                    id_criterio = ?,
                    id_rubrica = ?,
                    tipo_evidencia = ?,
                    nombre_evidencia = ?,
                    descripcion = ?,
                    fecha_entrega = ?,
                    estado_entrega = ?
                WHERE id_evidencia = ?
                """,
                (
                    id_estudiante_nuevo,
                    id_curso_editar,
                    id_criterio_nuevo,
                    id_rubrica_nueva,
                    editar_tipo_evidencia,
                    editar_nombre_evidencia,
                    editar_descripcion,
                    editar_fecha_entrega,
                    editar_estado_entrega,
                    id_evidencia_editar
                )
            )
            st.success("Evidencia actualizada correctamente.")
            st.rerun()

    # =========================
    # ELIMINAR EVIDENCIA
    # =========================
    st.markdown("### Eliminar evidencia")

    evidencia_eliminar_label = st.selectbox(
        "Selecciona la evidencia a eliminar",
        list(opciones_evidencias.keys()),
        key="evidencia_eliminar_select"
    )

    id_evidencia_eliminar = opciones_evidencias[evidencia_eliminar_label]

    if st.button("Eliminar evidencia"):
        total_retro = fetch_one(
            "SELECT COUNT(*) AS total FROM retroalimentaciones WHERE id_evidencia = ?",
            (id_evidencia_eliminar,)
        )["total"]

        if total_retro > 0:
            st.error("No se puede eliminar esta evidencia porque tiene retroalimentaciones asociadas.")
        else:
            execute_query(
                "DELETE FROM evidencias WHERE id_evidencia = ?",
                (id_evidencia_eliminar,)
            )
            st.success("Evidencia eliminada correctamente.")
            st.rerun()