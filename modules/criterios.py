import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one

def mostrar_criterios():
    st.subheader("📝 Gestión de Criterios de Evaluación")

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
    # REGISTRAR CRITERIO
    # =========================
    st.markdown("### Registrar criterio")

    with st.form("form_criterio"):
        curso_label = st.selectbox("Curso", list(opciones_cursos.keys()))
        competencia = st.text_input("Competencia")
        criterio = st.text_input("Criterio de evaluación")
        descripcion = st.text_area("Descripción")
        ponderacion = st.number_input("Ponderación", min_value=0.0, step=1.0)
        submitted = st.form_submit_button("Guardar criterio")

    if submitted:
        id_curso = opciones_cursos[curso_label]

        if not competencia.strip():
            st.error("La competencia es obligatoria.")
        elif not criterio.strip():
            st.error("El criterio de evaluación es obligatorio.")
        else:
            execute_query(
                """
                INSERT INTO criterios_evaluacion (
                    id_curso,
                    competencia,
                    criterio,
                    descripcion,
                    ponderacion
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    id_curso,
                    competencia,
                    criterio,
                    descripcion,
                    ponderacion
                )
            )
            st.success("Criterio registrado correctamente.")

    # =========================
    # LISTA DE CRITERIOS
    # =========================
    st.markdown("### Lista de criterios")

    criterios = fetch_all(
        """
        SELECT
            ce.id_criterio,
            ce.id_curso,
            c.nombre_curso,
            ce.competencia,
            ce.criterio,
            ce.descripcion,
            ce.ponderacion,
            ce.estado
        FROM criterios_evaluacion ce
        INNER JOIN cursos c ON ce.id_curso = c.id_curso
        ORDER BY ce.id_criterio DESC
        """
    )

    if criterios:
        df = pd.DataFrame([dict(row) for row in criterios])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay criterios registrados.")
        return

    # =========================
    # EDITAR CRITERIO
    # =========================
    st.markdown("### Editar criterio")

    opciones_criterios = {
        f"{criterio['id_criterio']} - {criterio['criterio']} ({criterio['nombre_curso']})": criterio["id_criterio"]
        for criterio in criterios
    }

    criterio_editar_label = st.selectbox(
        "Selecciona el criterio a editar",
        list(opciones_criterios.keys()),
        key="criterio_editar_select"
    )

    id_criterio_editar = opciones_criterios[criterio_editar_label]

    criterio_actual = fetch_one(
        """
        SELECT *
        FROM criterios_evaluacion
        WHERE id_criterio = ?
        """,
        (id_criterio_editar,)
    )

    curso_actual_id = criterio_actual["id_curso"] if criterio_actual else None
    labels_cursos = list(opciones_cursos.keys())
    index_curso_actual = 0

    for i, label in enumerate(labels_cursos):
        if opciones_cursos[label] == curso_actual_id:
            index_curso_actual = i
            break

    with st.form("form_editar_criterio"):
        editar_curso_label = st.selectbox(
            "Curso",
            labels_cursos,
            index=index_curso_actual
        )
        editar_competencia = st.text_input(
            "Competencia",
            value=criterio_actual["competencia"] if criterio_actual else ""
        )
        editar_criterio = st.text_input(
            "Criterio de evaluación",
            value=criterio_actual["criterio"] if criterio_actual else ""
        )
        editar_descripcion = st.text_area(
            "Descripción",
            value=criterio_actual["descripcion"] if criterio_actual and criterio_actual["descripcion"] else ""
        )
        editar_ponderacion = st.number_input(
            "Ponderación",
            min_value=0.0,
            step=1.0,
            value=float(criterio_actual["ponderacion"]) if criterio_actual and criterio_actual["ponderacion"] is not None else 0.0
        )
        editar_estado = st.selectbox(
            "Estado",
            ["Activo", "Inactivo"],
            index=0 if not criterio_actual or criterio_actual["estado"] == "Activo" else 1
        )

        submitted_editar = st.form_submit_button("Actualizar criterio")

    if submitted_editar:
        id_curso_nuevo = opciones_cursos[editar_curso_label]

        if not editar_competencia.strip():
            st.error("La competencia es obligatoria.")
        elif not editar_criterio.strip():
            st.error("El criterio de evaluación es obligatorio.")
        else:
            execute_query(
                """
                UPDATE criterios_evaluacion
                SET id_curso = ?,
                    competencia = ?,
                    criterio = ?,
                    descripcion = ?,
                    ponderacion = ?,
                    estado = ?
                WHERE id_criterio = ?
                """,
                (
                    id_curso_nuevo,
                    editar_competencia,
                    editar_criterio,
                    editar_descripcion,
                    editar_ponderacion,
                    editar_estado,
                    id_criterio_editar
                )
            )
            st.success("Criterio actualizado correctamente.")
            st.rerun()

    # =========================
    # ELIMINAR CRITERIO
    # =========================
    st.markdown("### Eliminar criterio")

    criterio_eliminar_label = st.selectbox(
        "Selecciona el criterio a eliminar",
        list(opciones_criterios.keys()),
        key="criterio_eliminar_select"
    )

    id_criterio_eliminar = opciones_criterios[criterio_eliminar_label]

    if st.button("Eliminar criterio"):
        total_rubricas = fetch_one(
            "SELECT COUNT(*) AS total FROM rubricas WHERE id_criterio = ?",
            (id_criterio_eliminar,)
        )["total"]

        total_evidencias = fetch_one(
            "SELECT COUNT(*) AS total FROM evidencias WHERE id_criterio = ?",
            (id_criterio_eliminar,)
        )["total"]

        total_retro = fetch_one(
            "SELECT COUNT(*) AS total FROM retroalimentaciones WHERE id_criterio = ?",
            (id_criterio_eliminar,)
        )["total"]

        if total_rubricas > 0 or total_evidencias > 0 or total_retro > 0:
            st.error("No se puede eliminar este criterio porque tiene registros asociados.")
        else:
            execute_query(
                "DELETE FROM criterios_evaluacion WHERE id_criterio = ?",
                (id_criterio_eliminar,)
            )
            st.success("Criterio eliminado correctamente.")
            st.rerun()