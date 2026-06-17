import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one

def mostrar_configuracion():
    st.subheader("⚙️ Configuración institucional")

    config_actual = fetch_one(
        """
        SELECT *
        FROM configuracion
        ORDER BY id_configuracion DESC
        LIMIT 1
        """
    )

    with st.form("form_configuracion"):
        nombre_institucion = st.text_input(
            "Nombre de la institución",
            value=config_actual["nombre_institucion"] if config_actual else ""
        )

        periodo_actual = st.text_input(
            "Periodo académico actual",
            value=config_actual["periodo_actual"] if config_actual else ""
        )

        responsable_sistema = st.text_input(
            "Responsable del sistema",
            value=config_actual["responsable_sistema"] if config_actual else ""
        )

        correo_contacto = st.text_input(
            "Correo institucional o de contacto",
            value=config_actual["correo_contacto"] if config_actual else ""
        )

        logo_url = st.text_input(
            "Ruta o nombre del logo (opcional)",
            value=config_actual["logo_url"] if config_actual else ""
        )

        submitted = st.form_submit_button("Guardar configuración")

    if submitted:
        if not nombre_institucion.strip():
            st.error("El nombre de la institución es obligatorio.")
        else:
            if config_actual:
                execute_query(
                    """
                    UPDATE configuracion
                    SET nombre_institucion = ?,
                        periodo_actual = ?,
                        responsable_sistema = ?,
                        correo_contacto = ?,
                        logo_url = ?,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id_configuracion = ?
                    """,
                    (
                        nombre_institucion,
                        periodo_actual,
                        responsable_sistema,
                        correo_contacto,
                        logo_url,
                        config_actual["id_configuracion"]
                    )
                )
                st.success("Configuración actualizada correctamente.")
            else:
                execute_query(
                    """
                    INSERT INTO configuracion (
                        nombre_institucion,
                        periodo_actual,
                        responsable_sistema,
                        correo_contacto,
                        logo_url
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        nombre_institucion,
                        periodo_actual,
                        responsable_sistema,
                        correo_contacto,
                        logo_url
                    )
                )
                st.success("Configuración guardada correctamente.")

    st.markdown("### Datos actuales")

    datos = fetch_all(
        """
        SELECT
            id_configuracion,
            nombre_institucion,
            periodo_actual,
            responsable_sistema,
            correo_contacto,
            logo_url,
            fecha_actualizacion
        FROM configuracion
        ORDER BY id_configuracion DESC
        """
    )

    if datos:
        df = pd.DataFrame([dict(row) for row in datos])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay configuración registrada.")