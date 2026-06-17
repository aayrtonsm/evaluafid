import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one
from utils.validators import validar_estudiante

def mostrar_estudiantes():
    st.subheader("👩‍🎓 Gestión de Estudiantes")

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
    # REGISTRAR ESTUDIANTE
    # =========================
    st.markdown("### Registrar estudiante")

    with st.form("form_estudiante"):
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
        codigo_estudiante = st.text_input("Código de estudiante")
        dni = st.text_input("DNI")
        correo = st.text_input("Correo")
        telefono = st.text_input("Teléfono")
        curso_label = st.selectbox("Curso asignado", list(opciones_cursos.keys()))
        observaciones = st.text_area("Observaciones")
        submitted = st.form_submit_button("Guardar estudiante")

    if submitted:
        id_curso = opciones_cursos[curso_label]

        valido, mensaje = validar_estudiante(
            nombres,
            apellidos,
            codigo_estudiante,
            dni,
            id_curso
        )

        if not valido:
            st.error(mensaje)
        else:
            execute_query(
                """
                INSERT INTO estudiantes (
                    codigo_estudiante,
                    dni,
                    nombres,
                    apellidos,
                    correo,
                    telefono,
                    id_curso,
                    observaciones
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    codigo_estudiante,
                    dni,
                    nombres,
                    apellidos,
                    correo,
                    telefono,
                    id_curso,
                    observaciones
                )
            )
            st.success("Estudiante registrado correctamente.")

    # =========================
    # LISTA DE ESTUDIANTES
    # =========================
    st.markdown("### Lista de estudiantes")

    estudiantes = fetch_all(
        """
        SELECT
            e.id_estudiante,
            e.codigo_estudiante,
            e.dni,
            e.nombres,
            e.apellidos,
            e.correo,
            e.telefono,
            c.nombre_curso,
            c.ciclo,
            c.seccion,
            e.estado
        FROM estudiantes e
        INNER JOIN cursos c ON e.id_curso = c.id_curso
        ORDER BY e.id_estudiante DESC
        """
    )

    if estudiantes:
        df = pd.DataFrame([dict(row) for row in estudiantes])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay estudiantes registrados.")
        return

    # =========================
    # EDITAR ESTUDIANTE
    # =========================
    st.markdown("### Editar estudiante")

    opciones_estudiantes = {
        f"{estudiante['id_estudiante']} - {estudiante['apellidos']}, {estudiante['nombres']}": estudiante["id_estudiante"]
        for estudiante in estudiantes
    }

    estudiante_editar_label = st.selectbox(
        "Selecciona el estudiante a editar",
        list(opciones_estudiantes.keys()),
        key="estudiante_editar_select"
    )

    id_estudiante_editar = opciones_estudiantes[estudiante_editar_label]

    estudiante_actual = fetch_one(
        """
        SELECT *
        FROM estudiantes
        WHERE id_estudiante = ?
        """,
        (id_estudiante_editar,)
    )

    curso_actual_id = estudiante_actual["id_curso"] if estudiante_actual else None
    labels_cursos = list(opciones_cursos.keys())
    index_curso_actual = 0

    for i, label in enumerate(labels_cursos):
        if opciones_cursos[label] == curso_actual_id:
            index_curso_actual = i
            break

    with st.form("form_editar_estudiante"):
        editar_nombres = st.text_input(
            "Nombres",
            value=estudiante_actual["nombres"] if estudiante_actual else ""
        )
        editar_apellidos = st.text_input(
            "Apellidos",
            value=estudiante_actual["apellidos"] if estudiante_actual else ""
        )
        editar_codigo_estudiante = st.text_input(
            "Código de estudiante",
            value=estudiante_actual["codigo_estudiante"] if estudiante_actual and estudiante_actual["codigo_estudiante"] else ""
        )
        editar_dni = st.text_input(
            "DNI",
            value=estudiante_actual["dni"] if estudiante_actual and estudiante_actual["dni"] else ""
        )
        editar_correo = st.text_input(
            "Correo",
            value=estudiante_actual["correo"] if estudiante_actual and estudiante_actual["correo"] else ""
        )
        editar_telefono = st.text_input(
            "Teléfono",
            value=estudiante_actual["telefono"] if estudiante_actual and estudiante_actual["telefono"] else ""
        )
        editar_curso_label = st.selectbox(
            "Curso asignado",
            labels_cursos,
            index=index_curso_actual
        )
        editar_observaciones = st.text_area(
            "Observaciones",
            value=estudiante_actual["observaciones"] if estudiante_actual and estudiante_actual["observaciones"] else ""
        )
        editar_estado = st.selectbox(
            "Estado",
            ["Activo", "Inactivo"],
            index=0 if not estudiante_actual or estudiante_actual["estado"] == "Activo" else 1
        )

        submitted_editar = st.form_submit_button("Actualizar estudiante")

    if submitted_editar:
        id_curso_nuevo = opciones_cursos[editar_curso_label]

        valido, mensaje = validar_estudiante(
            editar_nombres,
            editar_apellidos,
            editar_codigo_estudiante,
            editar_dni,
            id_curso_nuevo
        )

        if not valido:
            st.error(mensaje)
        else:
            execute_query(
                """
                UPDATE estudiantes
                SET nombres = ?,
                    apellidos = ?,
                    codigo_estudiante = ?,
                    dni = ?,
                    correo = ?,
                    telefono = ?,
                    id_curso = ?,
                    observaciones = ?,
                    estado = ?
                WHERE id_estudiante = ?
                """,
                (
                    editar_nombres,
                    editar_apellidos,
                    editar_codigo_estudiante,
                    editar_dni,
                    editar_correo,
                    editar_telefono,
                    id_curso_nuevo,
                    editar_observaciones,
                    editar_estado,
                    id_estudiante_editar
                )
            )
            st.success("Estudiante actualizado correctamente.")
            st.rerun()

    # =========================
    # ELIMINAR ESTUDIANTE
    # =========================
    st.markdown("### Eliminar estudiante")

    estudiante_eliminar_label = st.selectbox(
        "Selecciona el estudiante a eliminar",
        list(opciones_estudiantes.keys()),
        key="estudiante_eliminar_select"
    )

    id_estudiante_eliminar = opciones_estudiantes[estudiante_eliminar_label]

    if st.button("Eliminar estudiante"):
        total_evidencias = fetch_one(
            "SELECT COUNT(*) AS total FROM evidencias WHERE id_estudiante = ?",
            (id_estudiante_eliminar,)
        )["total"]

        total_retro = fetch_one(
            "SELECT COUNT(*) AS total FROM retroalimentaciones WHERE id_estudiante = ?",
            (id_estudiante_eliminar,)
        )["total"]

        if total_evidencias > 0 or total_retro > 0:
            st.error("No se puede eliminar este estudiante porque tiene registros asociados.")
        else:
            execute_query(
                "DELETE FROM estudiantes WHERE id_estudiante = ?",
                (id_estudiante_eliminar,)
            )
            st.success("Estudiante eliminado correctamente.")
            st.rerun()