import streamlit as st
import pandas as pd
from io import BytesIO
from database.db import fetch_all
from utils.theme import titulo_seccion, tarjeta_reporte


COLUMNAS_AMIGABLES = {
    "nombre_curso": "Curso",
    "estudiante": "Estudiante",
    "nombre_evidencia": "Evidencia",
    "tipo_evidencia": "Tipo",
    "fecha_entrega": "Fecha de entrega",
    "estado_entrega": "Estado",
    "criterio": "Criterio",
    "nombre_nivel": "Nivel",
    "puntaje": "Puntaje",
    "comentario_docente": "Comentario docente",
    "recomendacion_mejora": "Recomendación de mejora",
    "fecha_registro": "Fecha de registro",
}


def convertir_a_excel(df):
    """Convierte un DataFrame a Excel. Si falta openpyxl, devuelve None para no mostrar error rojo."""
    try:
        import openpyxl  # noqa: F401
    except ModuleNotFoundError:
        return None

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Reporte")
    output.seek(0)
    return output


def convertir_a_csv(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def mostrar_reportes():
    titulo_seccion(
        "📈 Reportes académicos",
        "Consulta el desempeño individual por curso, evidencia, criterio, nivel y retroalimentación."
    )

    cursos = fetch_all(
        """
        SELECT id_curso, nombre_curso, ciclo, seccion
        FROM cursos
        ORDER BY nombre_curso
        """
    )

    if not cursos:
        st.warning("Primero debes registrar al menos un curso para generar reportes.")
        return

    opciones_cursos = {
        f"{curso['nombre_curso']} | Ciclo {curso['ciclo']} | Sección {curso['seccion']}": curso["id_curso"]
        for curso in cursos
    }

    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            curso_label = st.selectbox("Curso", list(opciones_cursos.keys()))
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

        opciones_estudiantes = {
            f"{estudiante['apellidos']}, {estudiante['nombres']}": estudiante["id_estudiante"]
            for estudiante in estudiantes
        }

        with c2:
            estudiante_label = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
            id_estudiante = opciones_estudiantes[estudiante_label]

    reporte = fetch_all(
        """
        SELECT
            c.nombre_curso,
            es.apellidos || ', ' || es.nombres AS estudiante,
            e.nombre_evidencia,
            e.tipo_evidencia,
            e.fecha_entrega,
            e.estado_entrega,
            ce.criterio,
            nr.nombre_nivel,
            nr.puntaje,
            r.comentario_docente,
            r.recomendacion_mejora,
            r.fecha_registro
        FROM retroalimentaciones r
        INNER JOIN evidencias e ON r.id_evidencia = e.id_evidencia
        INNER JOIN estudiantes es ON r.id_estudiante = es.id_estudiante
        INNER JOIN cursos c ON e.id_curso = c.id_curso
        INNER JOIN criterios_evaluacion ce ON r.id_criterio = ce.id_criterio
        INNER JOIN niveles_rubrica nr ON r.id_nivel = nr.id_nivel
        WHERE r.id_estudiante = ? AND e.id_curso = ?
        ORDER BY r.id_retroalimentacion DESC
        """,
        (id_estudiante, id_curso)
    )

    if not reporte:
        st.info("Ese estudiante aún no tiene retroalimentaciones registradas.")
        return

    df = pd.DataFrame([dict(row) for row in reporte])
    df_visual = df.rename(columns=COLUMNAS_AMIGABLES)

    tarjeta_reporte(
        curso=df.iloc[0]["nombre_curso"],
        estudiante=df.iloc[0]["estudiante"],
        total=len(df)
    )

    titulo_seccion("Reporte individual", "Detalle completo de la evaluación registrada.")
    st.dataframe(df_visual, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    titulo_seccion("Exportación", "Descarga el reporte para archivo institucional o seguimiento académico.")

    nombre_base = df.iloc[0]["estudiante"].replace(", ", "_").replace(" ", "_")
    archivo_excel = convertir_a_excel(df_visual)

    col1, col2 = st.columns([1, 1])
    with col1:
        if archivo_excel is not None:
            st.download_button(
                label="⬇️ Descargar reporte en Excel",
                data=archivo_excel,
                file_name=f"reporte_{nombre_base}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        else:
            st.warning("Para descargar Excel instala openpyxl: `python -m pip install openpyxl`. Mientras tanto puedes descargar CSV.")

    with col2:
        st.download_button(
            label="⬇️ Descargar reporte en CSV",
            data=convertir_a_csv(df_visual),
            file_name=f"reporte_{nombre_base}.csv",
            mime="text/csv",
            use_container_width=True,
        )
