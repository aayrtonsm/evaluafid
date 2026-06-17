import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one

def mostrar_retroalimentacion():
    st.subheader("💬 Gestión de Retroalimentación")

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
    # REGISTRAR RETROALIMENTACIÓN
    # =========================
    st.markdown("### Registrar retroalimentación")

    curso_label = st.selectbox("Curso", list(opciones_cursos.keys()), key="curso_retro_nuevo")
    id_curso = opciones_cursos[curso_label]

    evidencias = fetch_all(
        """
        SELECT
            e.id_evidencia,
            es.apellidos || ', ' || es.nombres AS estudiante,
            e.nombre_evidencia
        FROM evidencias e
        INNER JOIN estudiantes es ON e.id_estudiante = es.id_estudiante
        WHERE e.id_curso = ?
        ORDER BY e.id_evidencia DESC
        """,
        (id_curso,)
    )

    if not evidencias:
        st.warning("Ese curso aún no tiene evidencias registradas.")
        return

    opciones_evidencias = {
        f"{evidencia['estudiante']} | {evidencia['nombre_evidencia']}": evidencia["id_evidencia"]
        for evidencia in evidencias
    }

    evidencia_label = st.selectbox("Evidencia", list(opciones_evidencias.keys()), key="evidencia_retro_nuevo")
    id_evidencia = opciones_evidencias[evidencia_label]

    datos_evidencia = fetch_one(
        """
        SELECT
            e.id_estudiante,
            e.id_criterio,
            e.id_rubrica
        FROM evidencias e
        WHERE e.id_evidencia = ?
        """,
        (id_evidencia,)
    )

    if not datos_evidencia:
        st.error("No se pudo recuperar la evidencia seleccionada.")
        return

    id_estudiante = datos_evidencia["id_estudiante"]
    id_criterio = datos_evidencia["id_criterio"]
    id_rubrica = datos_evidencia["id_rubrica"]

    if not id_rubrica:
        st.warning("La evidencia seleccionada no tiene una rúbrica asociada.")
        return

    niveles = fetch_all(
        """
        SELECT id_nivel, nombre_nivel, puntaje
        FROM niveles_rubrica
        WHERE id_rubrica = ?
        ORDER BY orden_nivel
        """,
        (id_rubrica,)
    )

    if not niveles:
        st.warning("La rúbrica asociada no tiene niveles registrados.")
        return

    opciones_niveles = {
        f"{nivel['nombre_nivel']} (Puntaje: {nivel['puntaje']})": nivel["id_nivel"]
        for nivel in niveles
    }

    with st.form("form_retroalimentacion"):
        nivel_label = st.selectbox("Nivel alcanzado", list(opciones_niveles.keys()))
        comentario_docente = st.text_area("Comentario del docente")
        recomendacion_mejora = st.text_area("Recomendación de mejora")
        submitted = st.form_submit_button("Guardar retroalimentación")

    if submitted:
        id_nivel = opciones_niveles[nivel_label]

        if not comentario_docente.strip():
            st.error("El comentario del docente es obligatorio.")
        else:
            execute_query(
                """
                INSERT INTO retroalimentaciones (
                    id_evidencia,
                    id_estudiante,
                    id_criterio,
                    id_nivel,
                    comentario_docente,
                    recomendacion_mejora
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    id_evidencia,
                    id_estudiante,
                    id_criterio,
                    id_nivel,
                    comentario_docente,
                    recomendacion_mejora
                )
            )
            st.success("Retroalimentación registrada correctamente.")

    # =========================
    # LISTA DE RETROALIMENTACIONES
    # =========================
    st.markdown("### Lista de retroalimentaciones")

    retroalimentaciones = fetch_all(
        """
        SELECT
            r.id_retroalimentacion,
            r.id_evidencia,
            r.id_estudiante,
            r.id_criterio,
            r.id_nivel,
            es.apellidos || ', ' || es.nombres AS estudiante,
            e.nombre_evidencia,
            nr.nombre_nivel,
            r.comentario_docente,
            r.recomendacion_mejora,
            r.fecha_registro
        FROM retroalimentaciones r
        INNER JOIN evidencias e ON r.id_evidencia = e.id_evidencia
        INNER JOIN estudiantes es ON r.id_estudiante = es.id_estudiante
        INNER JOIN niveles_rubrica nr ON r.id_nivel = nr.id_nivel
        ORDER BY r.id_retroalimentacion DESC
        """
    )

    if retroalimentaciones:
        df = pd.DataFrame([dict(row) for row in retroalimentaciones])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay retroalimentaciones registradas.")
        return

    # =========================
    # EDITAR RETROALIMENTACIÓN
    # =========================
    st.markdown("### Editar retroalimentación")

    opciones_retro = {
        f"{retro['id_retroalimentacion']} - {retro['estudiante']} | {retro['nombre_evidencia']}": retro["id_retroalimentacion"]
        for retro in retroalimentaciones
    }

    retro_editar_label = st.selectbox(
        "Selecciona la retroalimentación a editar",
        list(opciones_retro.keys()),
        key="retro_editar_select"
    )

    id_retro_editar = opciones_retro[retro_editar_label]

    retro_actual = fetch_one(
        """
        SELECT *
        FROM retroalimentaciones
        WHERE id_retroalimentacion = ?
        """,
        (id_retro_editar,)
    )

    evidencia_actual = fetch_one(
        """
        SELECT
            e.id_evidencia,
            e.id_estudiante,
            e.id_criterio,
            e.id_rubrica,
            es.apellidos || ', ' || es.nombres AS estudiante,
            e.nombre_evidencia
        FROM evidencias e
        INNER JOIN estudiantes es ON e.id_estudiante = es.id_estudiante
        WHERE e.id_evidencia = ?
        """,
        (retro_actual["id_evidencia"],)
    )

    rubrica_actual_id = evidencia_actual["id_rubrica"] if evidencia_actual else None

    niveles_editar = fetch_all(
        """
        SELECT id_nivel, nombre_nivel, puntaje
        FROM niveles_rubrica
        WHERE id_rubrica = ?
        ORDER BY orden_nivel
        """,
        (rubrica_actual_id,)
    )

    opciones_niveles_editar = {
        f"{nivel['nombre_nivel']} (Puntaje: {nivel['puntaje']})": nivel["id_nivel"]
        for nivel in niveles_editar
    }

    labels_niveles = list(opciones_niveles_editar.keys())
    index_nivel_actual = 0

    for i, label in enumerate(labels_niveles):
        if opciones_niveles_editar[label] == retro_actual["id_nivel"]:
            index_nivel_actual = i
            break

    with st.form("form_editar_retro"):
        st.text_input(
            "Evidencia seleccionada",
            value=f"{evidencia_actual['estudiante']} | {evidencia_actual['nombre_evidencia']}",
            disabled=True
        )

        editar_nivel_label = st.selectbox(
            "Nivel alcanzado",
            labels_niveles,
            index=index_nivel_actual
        )

        editar_comentario_docente = st.text_area(
            "Comentario del docente",
            value=retro_actual["comentario_docente"] if retro_actual else ""
        )

        editar_recomendacion_mejora = st.text_area(
            "Recomendación de mejora",
            value=retro_actual["recomendacion_mejora"] if retro_actual and retro_actual["recomendacion_mejora"] else ""
        )

        submitted_editar = st.form_submit_button("Actualizar retroalimentación")

    if submitted_editar:
        id_nivel_nuevo = opciones_niveles_editar[editar_nivel_label]

        if not editar_comentario_docente.strip():
            st.error("El comentario del docente es obligatorio.")
        else:
            execute_query(
                """
                UPDATE retroalimentaciones
                SET id_nivel = ?,
                    comentario_docente = ?,
                    recomendacion_mejora = ?
                WHERE id_retroalimentacion = ?
                """,
                (
                    id_nivel_nuevo,
                    editar_comentario_docente,
                    editar_recomendacion_mejora,
                    id_retro_editar
                )
            )
            st.success("Retroalimentación actualizada correctamente.")
            st.rerun()

    # =========================
    # ELIMINAR RETROALIMENTACIÓN
    # =========================
    st.markdown("### Eliminar retroalimentación")

    retro_eliminar_label = st.selectbox(
        "Selecciona la retroalimentación a eliminar",
        list(opciones_retro.keys()),
        key="retro_eliminar_select"
    )

    id_retro_eliminar = opciones_retro[retro_eliminar_label]

    if st.button("Eliminar retroalimentación"):
        execute_query(
            "DELETE FROM retroalimentaciones WHERE id_retroalimentacion = ?",
            (id_retro_eliminar,)
        )
        st.success("Retroalimentación eliminada correctamente.")
        st.rerun()