import hashlib
import streamlit as st
from database.db import fetch_one

def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

def login():
    _, col, _ = st.columns([1.15, 1, 1.15])

    with col:
        st.markdown(
            """
            <div class="login-intro">
                <div class="login-title">🔐 Acceso al sistema</div>
                <div class="login-subtitle">
                    Ingresa tus credenciales para continuar con la gestión académica.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("form_login", clear_on_submit=False):
            usuario = st.text_input("Usuario", placeholder="Ejemplo: admin")
            clave = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            submitted = st.form_submit_button("Ingresar al sistema", use_container_width=True)

        if submitted:
            usuario_db = fetch_one(
                """
                SELECT *
                FROM usuarios
                WHERE nombre_usuario = ? AND estado = 'Activo'
                """,
                (usuario.strip(),)
            )

            if usuario_db and usuario_db["clave_hash"] == hash_clave(clave):
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = usuario_db["nombre_usuario"]
                st.session_state["rol"] = usuario_db["rol"]
                st.session_state["nombre_completo"] = usuario_db["nombre_completo"]
                st.success("Acceso correcto.")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

def logout():
    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        st.session_state["autenticado"] = False
        st.session_state["usuario"] = None
        st.session_state["rol"] = None
        st.session_state["nombre_completo"] = None
        st.rerun()

def esta_autenticado():
    return st.session_state.get("autenticado", False)
