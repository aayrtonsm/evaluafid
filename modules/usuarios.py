import hashlib
import streamlit as st
import pandas as pd
from database.db import execute_query, fetch_all, fetch_one

def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

def mostrar_usuarios():
    st.subheader("👤 Gestión de usuarios")

    st.markdown("### Crear nuevo usuario")

    with st.form("form_usuario"):
        nombre_usuario = st.text_input("Nombre de usuario")
        clave = st.text_input("Contraseña", type="password")
        nombre_completo = st.text_input("Nombre completo")
        correo = st.text_input("Correo")
        rol = st.selectbox("Rol", ["Administrador", "Docente"])
        estado = st.selectbox("Estado", ["Activo", "Inactivo"])

        submitted = st.form_submit_button("Guardar usuario")

    if submitted:
        if not nombre_usuario.strip():
            st.error("El nombre de usuario es obligatorio.")
        elif not clave.strip():
            st.error("La contraseña es obligatoria.")
        else:
            existe = fetch_one(
                """
                SELECT *
                FROM usuarios
                WHERE nombre_usuario = ?
                """,
                (nombre_usuario,)
            )

            if existe:
                st.warning("Ese nombre de usuario ya existe.")
            else:
                execute_query(
                    """
                    INSERT INTO usuarios (
                        nombre_usuario,
                        clave_hash,
                        rol,
                        estado,
                        nombre_completo,
                        correo
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nombre_usuario,
                        hash_clave(clave),
                        rol,
                        estado,
                        nombre_completo,
                        correo
                    )
                )
                st.success("Usuario registrado correctamente.")

    st.markdown("### Lista de usuarios")

    usuarios = fetch_all(
        """
        SELECT
            id_usuario,
            nombre_usuario,
            nombre_completo,
            correo,
            rol,
            estado,
            fecha_creacion
        FROM usuarios
        ORDER BY id_usuario DESC
        """
    )

    if usuarios:
        df = pd.DataFrame([dict(row) for row in usuarios])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay usuarios registrados.")