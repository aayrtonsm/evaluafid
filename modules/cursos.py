import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one
from utils.validators import validar_curso

def mostrar_cursos():
    st.subheader("📘 Gestión de Cursos / Módulos")

    # =========================
    # REGISTRAR CURSO
    # =========================
    st.markdown("### Registrar curso")

    with st.form("form_curso"):
        nombre_curso = st.text_input("Nombre del curso o módulo")
        programa_estudios = st.text_input("Programa de estudios")
        ciclo = st.text_input("Ciclo")
        periodo_academico = st.text_input("Periodo académico")
        seccion = st.text_input("Sección")
        descripcion = st.text_area("Descripción")
        docente_responsable = st.text_input("Docente responsable")
        submitted = st.form_submit_button("Guardar curso")

    if submitted:
        valido, mensaje = validar_curso(
            nombre_curso,
            programa_estudios,
            ciclo,
            periodo_academico,
            seccion
        )

        if not valido:
            st.error(mensaje)
        else:
            existe = fetch_one(
                """
                SELECT * FROM cursos
                WHERE nombre_curso = ? AND ciclo = ? AND periodo_academico = ? AND seccion = ?
                """,
                (nombre_curso, ciclo, periodo_academico, seccion)
            )

            if existe:
                st.warning("Ya existe un curso con ese nombre, ciclo, periodo y sección.")
            else:
                execute_query(
                    """
                    INSERT INTO cursos (
                        nombre_curso,
                        programa_estudios,
                        ciclo,
                        periodo_academico,
                        seccion,
                        descripcion,
                        docente_responsable
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nombre_curso,
                        programa_estudios,
                        ciclo,
                        periodo_academico,
                        seccion,
                        descripcion,
                        docente_responsable
                    )
                )
                st.success("Curso registrado correctamente.")

    # =========================
    # LISTA DE CURSOS
    # =========================
    st.markdown("### Lista de cursos")

    cursos = fetch_all(
        """
        SELECT
            id_curso,
            nombre_curso,
            programa_estudios,
            ciclo,
            periodo_academico,
            seccion,
            docente_responsable,
            estado
        FROM cursos
        ORDER BY id_curso DESC
        """
    )

    if cursos:
        df = pd.DataFrame([dict(row) for row in cursos])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay cursos registrados.")
        return

    # =========================
    # EDITAR CURSO
    # =========================
    st.markdown("### Editar curso")

    opciones_cursos = {
        f"{curso['id_curso']} - {curso['nombre_curso']} | Ciclo {curso['ciclo']} | Sección {curso['seccion']}": curso["id_curso"]
        for curso in cursos
    }

    curso_editar_label = st.selectbox(
        "Selecciona el curso a editar",
        list(opciones_cursos.keys()),
        key="curso_editar_select"
    )

    id_curso_editar = opciones_cursos[curso_editar_label]

    curso_actual = fetch_one(
        """
        SELECT *
        FROM cursos
        WHERE id_curso = ?
        """,
        (id_curso_editar,)
    )

    with st.form("form_editar_curso"):
        editar_nombre_curso = st.text_input(
            "Nombre del curso o módulo",
            value=curso_actual["nombre_curso"] if curso_actual else ""
        )
        editar_programa_estudios = st.text_input(
            "Programa de estudios",
            value=curso_actual["programa_estudios"] if curso_actual else ""
        )
        editar_ciclo = st.text_input(
            "Ciclo",
            value=curso_actual["ciclo"] if curso_actual else ""
        )
        editar_periodo_academico = st.text_input(
            "Periodo académico",
            value=curso_actual["periodo_academico"] if curso_actual else ""
        )
        editar_seccion = st.text_input(
            "Sección",
            value=curso_actual["seccion"] if curso_actual else ""
        )
        editar_descripcion = st.text_area(
            "Descripción",
            value=curso_actual["descripcion"] if curso_actual and curso_actual["descripcion"] else ""
        )
        editar_docente_responsable = st.text_input(
            "Docente responsable",
            value=curso_actual["docente_responsable"] if curso_actual and curso_actual["docente_responsable"] else ""
        )
        editar_estado = st.selectbox(
            "Estado",
            ["Activo", "Inactivo"],
            index=0 if not curso_actual or curso_actual["estado"] == "Activo" else 1
        )

        submitted_editar = st.form_submit_button("Actualizar curso")

    if submitted_editar:
        valido, mensaje = validar_curso(
            editar_nombre_curso,
            editar_programa_estudios,
            editar_ciclo,
            editar_periodo_academico,
            editar_seccion
        )

        if not valido:
            st.error(mensaje)
        else:
            execute_query(
                """
                UPDATE cursos
                SET nombre_curso = ?,
                    programa_estudios = ?,
                    ciclo = ?,
                    periodo_academico = ?,
                    seccion = ?,
                    descripcion = ?,
                    docente_responsable = ?,
                    estado = ?
                WHERE id_curso = ?
                """,
                (
                    editar_nombre_curso,
                    editar_programa_estudios,
                    editar_ciclo,
                    editar_periodo_academico,
                    editar_seccion,
                    editar_descripcion,
                    editar_docente_responsable,
                    editar_estado,
                    id_curso_editar
                )
            )
            st.success("Curso actualizado correctamente.")
            st.rerun()

    # =========================
    # ELIMINAR CURSO
    # =========================
    st.markdown("### Eliminar curso")

    curso_eliminar_label = st.selectbox(
        "Selecciona el curso a eliminar",
        list(opciones_cursos.keys()),
        key="curso_eliminar_select"
    )

    id_curso_eliminar = opciones_cursos[curso_eliminar_label]

    if st.button("Eliminar curso"):
        total_estudiantes = fetch_one(
            "SELECT COUNT(*) AS total FROM estudiantes WHERE id_curso = ?",
            (id_curso_eliminar,)
        )["total"]

        total_criterios = fetch_one(
            "SELECT COUNT(*) AS total FROM criterios_evaluacion WHERE id_curso = ?",
            (id_curso_eliminar,)
        )["total"]

        total_rubricas = fetch_one(
            "SELECT COUNT(*) AS total FROM rubricas WHERE id_curso = ?",
            (id_curso_eliminar,)
        )["total"]

        total_evidencias = fetch_one(
            "SELECT COUNT(*) AS total FROM evidencias WHERE id_curso = ?",
            (id_curso_eliminar,)
        )["total"]

        if total_estudiantes > 0 or total_criterios > 0 or total_rubricas > 0 or total_evidencias > 0:
            st.error("No se puede eliminar este curso porque tiene registros asociados.")
        else:
            execute_query(
                "DELETE FROM cursos WHERE id_curso = ?",
                (id_curso_eliminar,)
            )
            st.success("Curso eliminado correctamente.")
            st.rerun()