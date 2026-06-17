import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one

def mostrar_rubricas():
    st.subheader("📊 Gestión de Rúbricas")

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
    # REGISTRAR RÚBRICA
    # =========================
    st.markdown("### Registrar rúbrica")

    curso_label = st.selectbox("Curso", list(opciones_cursos.keys()), key="curso_rubrica_nuevo")
    id_curso = opciones_cursos[curso_label]

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

    opciones_criterios = {
        criterio["criterio"]: criterio["id_criterio"]
        for criterio in criterios
    }

    with st.form("form_rubrica"):
        criterio_label = st.selectbox("Criterio de evaluación", list(opciones_criterios.keys()))
        nombre_rubrica = st.text_input("Nombre de la rúbrica")
        descripcion = st.text_area("Descripción general")

        nivel_1 = st.text_input("Nivel 1", value="Previo al inicio")
        descriptor_1 = st.text_area("Descriptor nivel 1")
        puntaje_1 = st.number_input("Puntaje nivel 1", min_value=1.0, step=1.0, value=1.0)

        nivel_2 = st.text_input("Nivel 2", value="Inicio")
        descriptor_2 = st.text_area("Descriptor nivel 2")
        puntaje_2 = st.number_input("Puntaje nivel 2", min_value=1.0, step=1.0, value=2.0)

        nivel_3 = st.text_input("Nivel 3", value="En proceso")
        descriptor_3 = st.text_area("Descriptor nivel 3")
        puntaje_3 = st.number_input("Puntaje nivel 3", min_value=1.0, step=1.0, value=3.0)

        nivel_4 = st.text_input("Nivel 4", value="Logrado")
        descriptor_4 = st.text_area("Descriptor nivel 4")
        puntaje_4 = st.number_input("Puntaje nivel 4", min_value=1.0, step=1.0, value=4.0)

        nivel_5 = st.text_input("Nivel 5", value="Destacado")
        descriptor_5 = st.text_area("Descriptor nivel 5")
        puntaje_5 = st.number_input("Puntaje nivel 5", min_value=1.0, step=1.0, value=5.0)

        submitted = st.form_submit_button("Guardar rúbrica")

    if submitted:
        id_criterio = opciones_criterios[criterio_label]

        if not nombre_rubrica.strip():
            st.error("El nombre de la rúbrica es obligatorio.")
        else:
            execute_query(
                """
                INSERT INTO rubricas (
                    id_curso,
                    id_criterio,
                    nombre_rubrica,
                    descripcion
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    id_curso,
                    id_criterio,
                    nombre_rubrica,
                    descripcion
                )
            )

            rubrica = fetch_one(
                """
                SELECT id_rubrica
                FROM rubricas
                ORDER BY id_rubrica DESC
                LIMIT 1
                """
            )

            id_rubrica = rubrica["id_rubrica"]

            niveles = [
                (nivel_1, descriptor_1, puntaje_1, 1),
                (nivel_2, descriptor_2, puntaje_2, 2),
                (nivel_3, descriptor_3, puntaje_3, 3),
                (nivel_4, descriptor_4, puntaje_4, 4),
                (nivel_5, descriptor_5, puntaje_5, 5),
            ]

            for nombre_nivel, descriptor, puntaje, orden in niveles:
                execute_query(
                    """
                    INSERT INTO niveles_rubrica (
                        id_rubrica,
                        nombre_nivel,
                        descriptor,
                        puntaje,
                        orden_nivel
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        id_rubrica,
                        nombre_nivel,
                        descriptor,
                        puntaje,
                        orden
                    )
                )

            st.success("Rúbrica registrada correctamente.")

    # =========================
    # LISTA DE RÚBRICAS
    # =========================
    st.markdown("### Lista de rúbricas")

    rubricas = fetch_all(
        """
        SELECT
            r.id_rubrica,
            r.id_curso,
            r.id_criterio,
            c.nombre_curso,
            ce.criterio,
            r.nombre_rubrica,
            r.descripcion,
            r.estado
        FROM rubricas r
        INNER JOIN cursos c ON r.id_curso = c.id_curso
        INNER JOIN criterios_evaluacion ce ON r.id_criterio = ce.id_criterio
        ORDER BY r.id_rubrica DESC
        """
    )

    if rubricas:
        df = pd.DataFrame([dict(row) for row in rubricas])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay rúbricas registradas.")
        return

    # =========================
    # EDITAR RÚBRICA
    # =========================
    st.markdown("### Editar rúbrica")

    opciones_rubricas = {
        f"{rubrica['id_rubrica']} - {rubrica['nombre_rubrica']} ({rubrica['nombre_curso']})": rubrica["id_rubrica"]
        for rubrica in rubricas
    }

    rubrica_editar_label = st.selectbox(
        "Selecciona la rúbrica a editar",
        list(opciones_rubricas.keys()),
        key="rubrica_editar_select"
    )

    id_rubrica_editar = opciones_rubricas[rubrica_editar_label]

    rubrica_actual = fetch_one(
        """
        SELECT *
        FROM rubricas
        WHERE id_rubrica = ?
        """,
        (id_rubrica_editar,)
    )

    niveles_actuales = fetch_all(
        """
        SELECT *
        FROM niveles_rubrica
        WHERE id_rubrica = ?
        ORDER BY orden_nivel
        """,
        (id_rubrica_editar,)
    )

    curso_actual_id = rubrica_actual["id_curso"] if rubrica_actual else None
    labels_cursos = list(opciones_cursos.keys())
    index_curso_actual = 0

    for i, label in enumerate(labels_cursos):
        if opciones_cursos[label] == curso_actual_id:
            index_curso_actual = i
            break

    curso_editar_label = st.selectbox(
        "Curso de la rúbrica",
        labels_cursos,
        index=index_curso_actual,
        key="rubrica_curso_editar"
    )

    id_curso_editar = opciones_cursos[curso_editar_label]

    criterios_editar = fetch_all(
        """
        SELECT id_criterio, criterio
        FROM criterios_evaluacion
        WHERE id_curso = ?
        ORDER BY id_criterio DESC
        """,
        (id_curso_editar,)
    )

    opciones_criterios_editar = {
        criterio["criterio"]: criterio["id_criterio"]
        for criterio in criterios_editar
    }

    criterio_actual_id = rubrica_actual["id_criterio"] if rubrica_actual else None
    labels_criterios = list(opciones_criterios_editar.keys())
    index_criterio_actual = 0

    for i, label in enumerate(labels_criterios):
        if opciones_criterios_editar[label] == criterio_actual_id:
            index_criterio_actual = i
            break

    def nivel_valor(indice, campo, default):
        if len(niveles_actuales) >= indice:
            valor = niveles_actuales[indice - 1][campo]
            return valor if valor is not None else default
        return default

    with st.form("form_editar_rubrica"):
        editar_criterio_label = st.selectbox(
            "Criterio de evaluación",
            labels_criterios,
            index=index_criterio_actual
        )
        editar_nombre_rubrica = st.text_input(
            "Nombre de la rúbrica",
            value=rubrica_actual["nombre_rubrica"] if rubrica_actual else ""
        )
        editar_descripcion = st.text_area(
            "Descripción general",
            value=rubrica_actual["descripcion"] if rubrica_actual and rubrica_actual["descripcion"] else ""
        )

        editar_nivel_1 = st.text_input("Nivel 1", value=nivel_valor(1, "nombre_nivel", "Previo al inicio"))
        editar_descriptor_1 = st.text_area("Descriptor nivel 1", value=nivel_valor(1, "descriptor", ""))
        editar_puntaje_1 = st.number_input("Puntaje nivel 1", min_value=1.0, step=1.0, value=float(nivel_valor(1, "puntaje", 1.0)))

        editar_nivel_2 = st.text_input("Nivel 2", value=nivel_valor(2, "nombre_nivel", "Inicio"))
        editar_descriptor_2 = st.text_area("Descriptor nivel 2", value=nivel_valor(2, "descriptor", ""))
        editar_puntaje_2 = st.number_input("Puntaje nivel 2", min_value=1.0, step=1.0, value=float(nivel_valor(2, "puntaje", 2.0)))

        editar_nivel_3 = st.text_input("Nivel 3", value=nivel_valor(3, "nombre_nivel", "En proceso"))
        editar_descriptor_3 = st.text_area("Descriptor nivel 3", value=nivel_valor(3, "descriptor", ""))
        editar_puntaje_3 = st.number_input("Puntaje nivel 3", min_value=1.0, step=1.0, value=float(nivel_valor(3, "puntaje", 3.0)))

        editar_nivel_4 = st.text_input("Nivel 4", value=nivel_valor(4, "nombre_nivel", "Logrado"))
        editar_descriptor_4 = st.text_area("Descriptor nivel 4", value=nivel_valor(4, "descriptor", ""))
        editar_puntaje_4 = st.number_input("Puntaje nivel 4", min_value=1.0, step=1.0, value=float(nivel_valor(4, "puntaje", 4.0)))

        editar_nivel_5 = st.text_input("Nivel 5", value=nivel_valor(5, "nombre_nivel", "Destacado"))
        editar_descriptor_5 = st.text_area("Descriptor nivel 5", value=nivel_valor(5, "descriptor", ""))
        editar_puntaje_5 = st.number_input("Puntaje nivel 5", min_value=1.0, step=1.0, value=float(nivel_valor(5, "puntaje", 5.0)))

        editar_estado = st.selectbox(
            "Estado",
            ["Activo", "Inactivo"],
            index=0 if not rubrica_actual or rubrica_actual["estado"] == "Activo" else 1
        )

        submitted_editar = st.form_submit_button("Actualizar rúbrica")

    if submitted_editar:
        id_criterio_nuevo = opciones_criterios_editar[editar_criterio_label]

        if not editar_nombre_rubrica.strip():
            st.error("El nombre de la rúbrica es obligatorio.")
        else:
            execute_query(
                """
                UPDATE rubricas
                SET id_curso = ?,
                    id_criterio = ?,
                    nombre_rubrica = ?,
                    descripcion = ?,
                    estado = ?
                WHERE id_rubrica = ?
                """,
                (
                    id_curso_editar,
                    id_criterio_nuevo,
                    editar_nombre_rubrica,
                    editar_descripcion,
                    editar_estado,
                    id_rubrica_editar
                )
            )

            execute_query(
                "DELETE FROM niveles_rubrica WHERE id_rubrica = ?",
                (id_rubrica_editar,)
            )

            niveles_editados = [
                (editar_nivel_1, editar_descriptor_1, editar_puntaje_1, 1),
                (editar_nivel_2, editar_descriptor_2, editar_puntaje_2, 2),
                (editar_nivel_3, editar_descriptor_3, editar_puntaje_3, 3),
                (editar_nivel_4, editar_descriptor_4, editar_puntaje_4, 4),
                (editar_nivel_5, editar_descriptor_5, editar_puntaje_5, 5),
            ]

            for nombre_nivel, descriptor, puntaje, orden in niveles_editados:
                execute_query(
                    """
                    INSERT INTO niveles_rubrica (
                        id_rubrica,
                        nombre_nivel,
                        descriptor,
                        puntaje,
                        orden_nivel
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        id_rubrica_editar,
                        nombre_nivel,
                        descriptor,
                        puntaje,
                        orden
                    )
                )

            st.success("Rúbrica actualizada correctamente.")
            st.rerun()

    # =========================
    # ELIMINAR RÚBRICA
    # =========================
    st.markdown("### Eliminar rúbrica")

    rubrica_eliminar_label = st.selectbox(
        "Selecciona la rúbrica a eliminar",
        list(opciones_rubricas.keys()),
        key="rubrica_eliminar_select"
    )

    id_rubrica_eliminar = opciones_rubricas[rubrica_eliminar_label]

    if st.button("Eliminar rúbrica"):
        total_evidencias = fetch_one(
            "SELECT COUNT(*) AS total FROM evidencias WHERE id_rubrica = ?",
            (id_rubrica_eliminar,)
        )["total"]

        if total_evidencias > 0:
            st.error("No se puede eliminar esta rúbrica porque tiene evidencias asociadas.")
        else:
            execute_query(
                "DELETE FROM niveles_rubrica WHERE id_rubrica = ?",
                (id_rubrica_eliminar,)
            )
            execute_query(
                "DELETE FROM rubricas WHERE id_rubrica = ?",
                (id_rubrica_eliminar,)
            )
            st.success("Rúbrica eliminada correctamente.")
            st.rerun()