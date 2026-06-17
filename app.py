import streamlit as st
from database.schema import create_tables
from database.db import fetch_one
from modules.cursos import mostrar_cursos
from modules.estudiantes import mostrar_estudiantes
from modules.criterios import mostrar_criterios
from modules.rubricas import mostrar_rubricas
from modules.evidencias import mostrar_evidencias
from modules.retroalimentacion import mostrar_retroalimentacion
from modules.reportes import mostrar_reportes
from modules.configuracion import mostrar_configuracion
from modules.usuarios import mostrar_usuarios
from utils.auth import login, logout, esta_autenticado
from utils.theme import (
    cargar_estilos,
    encabezado_principal,
    tarjeta_metrica,
    tarjeta_bienvenida,
    titulo_seccion,
    tarjeta_rapida
)

st.set_page_config(
    page_title="EvalúaFID",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

cargar_estilos()
create_tables()

def obtener_total(tabla, campo_id):
    fila = fetch_one(f"SELECT COUNT({campo_id}) AS total FROM {tabla}")
    return fila["total"] if fila else 0

def mostrar_sidebar():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-logo">EF</div>
            <div>
                <div class="sidebar-brand-title">EvalúaFID</div>
                <div class="sidebar-brand-subtitle">Evaluación formativa y gestión de evidencias</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    nombre = st.session_state.get("nombre_completo") or st.session_state.get("usuario") or "Usuario"
    rol = st.session_state.get("rol") or "Rol no definido"

    st.sidebar.markdown(
        f"""
        <div class="sidebar-user">
            <strong>{nombre}</strong><br>
            <span>{rol}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.sidebar.radio(
        "Menú principal",
        [
            "Inicio",
            "Usuarios",
            "Cursos",
            "Estudiantes",
            "Criterios",
            "Rúbricas",
            "Evidencias",
            "Retroalimentación",
            "Reportes",
            "Configuración"
        ],
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    logout()
    st.sidebar.caption("EvalúaFID v1.0")
    return menu

if not esta_autenticado():
    encabezado_principal(
        titulo="EvalúaFID",
        subtitulo="Sistema de evaluación formativa y gestión de evidencias para la Formación Inicial Docente",
        icono="📘",
        etiqueta="Acceso seguro"
    )
    login()
    st.stop()

total_cursos = obtener_total("cursos", "id_curso")
total_estudiantes = obtener_total("estudiantes", "id_estudiante")
total_criterios = obtener_total("criterios_evaluacion", "id_criterio")
total_rubricas = obtener_total("rubricas", "id_rubrica")
total_evidencias = obtener_total("evidencias", "id_evidencia")
total_retro = obtener_total("retroalimentaciones", "id_retroalimentacion")

menu = mostrar_sidebar()

encabezado_principal(
    titulo="EvalúaFID",
    subtitulo="Panel académico para administrar evaluación formativa, evidencias, rúbricas y reportes.",
    icono="📘",
    etiqueta=f"Sesión activa · {st.session_state.get('rol', 'Usuario')}"
)

if menu == "Inicio":
    tarjeta_bienvenida()

    titulo_seccion(
        "Resumen general",
        "Indicadores rápidos del estado actual del sistema."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        tarjeta_metrica("Cursos registrados", total_cursos, "📘")
    with col2:
        tarjeta_metrica("Estudiantes registrados", total_estudiantes, "👩‍🎓")
    with col3:
        tarjeta_metrica("Criterios registrados", total_criterios, "📝")

    col4, col5, col6 = st.columns(3)
    with col4:
        tarjeta_metrica("Rúbricas registradas", total_rubricas, "📊")
    with col5:
        tarjeta_metrica("Evidencias registradas", total_evidencias, "📂")
    with col6:
        tarjeta_metrica("Retroalimentaciones", total_retro, "💬")

    st.markdown("<br>", unsafe_allow_html=True)
    titulo_seccion("Accesos de trabajo", "Flujo sugerido para registrar y evaluar evidencias.")

    a1, a2, a3 = st.columns(3)
    with a1:
        tarjeta_rapida("1. Preparar cursos", "Registra cursos, estudiantes y criterios de evaluación.")
    with a2:
        tarjeta_rapida("2. Construir rúbricas", "Define niveles, descriptores y puntajes para evaluar.")
    with a3:
        tarjeta_rapida("3. Generar reportes", "Consulta evidencias, retroalimentaciones y exporta resultados.")

    st.info("Versión actual: v1.0 · Interfaz visual renovada.")

elif menu == "Usuarios":
    mostrar_usuarios()

elif menu == "Cursos":
    mostrar_cursos()

elif menu == "Estudiantes":
    mostrar_estudiantes()

elif menu == "Criterios":
    mostrar_criterios()

elif menu == "Rúbricas":
    mostrar_rubricas()

elif menu == "Evidencias":
    mostrar_evidencias()

elif menu == "Retroalimentación":
    mostrar_retroalimentacion()

elif menu == "Reportes":
    mostrar_reportes()

elif menu == "Configuración":
    mostrar_configuracion()
