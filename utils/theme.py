import streamlit as st


def cargar_estilos():
    """Carga el tema visual corporativo oscuro para EvalúaFID."""
    st.markdown(
        """
        <style>
            :root {
                --fid-bg-0: #06111F;
                --fid-bg-1: #0A1B2D;
                --fid-bg-2: #0F2438;
                --fid-bg-3: #132E48;
                --fid-card: rgba(15, 36, 56, 0.94);
                --fid-card-2: rgba(19, 46, 72, 0.96);
                --fid-border: rgba(148, 197, 253, 0.18);
                --fid-border-strong: rgba(125, 211, 252, 0.34);
                --fid-text: #F8FAFC;
                --fid-muted: #C9D6E8;
                --fid-soft: #8EABC9;
                --fid-primary: #38BDF8;
                --fid-primary-2: #2563EB;
                --fid-accent: #22C55E;
                --fid-warning: #F59E0B;
                --fid-danger: #FB7185;
                --fid-shadow: 0 22px 55px rgba(0, 0, 0, 0.30);
            }

            html, body, [class*="css"] {
                font-size: 18px !important;
            }

            .stApp {
                background:
                    radial-gradient(circle at 12% 8%, rgba(56,189,248,0.18), transparent 28%),
                    radial-gradient(circle at 88% 18%, rgba(37,99,235,0.18), transparent 30%),
                    linear-gradient(135deg, var(--fid-bg-0) 0%, var(--fid-bg-1) 47%, #071827 100%) !important;
                color: var(--fid-text) !important;
            }

            header[data-testid="stHeader"] {
                background: rgba(6, 17, 31, 0.10) !important;
                backdrop-filter: blur(12px);
            }

            .block-container {
                padding-top: 1.4rem !important;
                padding-bottom: 3rem !important;
                max-width: 1500px !important;
            }

            h1, h2, h3, h4, h5, h6,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {
                color: var(--fid-text) !important;
                letter-spacing: -0.035em;
                font-weight: 850 !important;
            }

            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li,
            [data-testid="stMarkdownContainer"] span {
                color: var(--fid-muted);
                font-size: 1.02rem;
                line-height: 1.62;
            }

            a { color: var(--fid-primary) !important; }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at top left, rgba(56,189,248,0.18), transparent 38%),
                    linear-gradient(180deg, #071B2D 0%, #0B2A45 48%, #0D3C66 100%) !important;
                border-right: 1px solid rgba(148,197,253,0.18);
            }

            section[data-testid="stSidebar"] .block-container {
                padding-top: 1.5rem !important;
            }

            section[data-testid="stSidebar"] * {
                color: #F8FAFC !important;
                font-size: 1.01rem;
            }

            .sidebar-brand {
                display: flex;
                gap: 13px;
                align-items: center;
                padding: 18px 16px;
                border-radius: 24px;
                background: rgba(255,255,255,0.075);
                border: 1px solid rgba(148,197,253,0.22);
                box-shadow: 0 16px 34px rgba(0,0,0,0.20);
                margin-bottom: 18px;
            }

            .brand-logo {
                width: 58px;
                height: 58px;
                flex: 0 0 58px;
                border-radius: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                background:
                    linear-gradient(135deg, rgba(56,189,248,0.95), rgba(37,99,235,0.96));
                box-shadow: 0 14px 30px rgba(56,189,248,0.20);
                border: 1px solid rgba(255,255,255,0.26);
                font-weight: 950;
                font-size: 1.25rem !important;
                letter-spacing: -0.06em;
            }

            .sidebar-brand-title {
                font-size: 1.42rem !important;
                font-weight: 950 !important;
                letter-spacing: -0.04em;
                line-height: 1.05;
                margin-bottom: 6px;
            }

            .sidebar-brand-subtitle {
                font-size: .88rem !important;
                color: #C9D6E8 !important;
                line-height: 1.36;
            }

            .sidebar-user {
                padding: 15px 16px;
                border-radius: 18px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(148,197,253,0.19);
                margin: 12px 0 17px 0;
                line-height: 1.45;
            }

            .sidebar-user strong {
                font-size: 1.05rem !important;
            }

            .sidebar-user span {
                color: #A9C6E8 !important;
                font-size: .92rem !important;
                font-weight: 650;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] label {
                background: rgba(255,255,255,0.065) !important;
                border: 1px solid rgba(148,197,253,0.13) !important;
                border-radius: 16px !important;
                padding: 11px 12px !important;
                margin-bottom: 9px !important;
                transition: all .18s ease;
                min-height: 44px;
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
                background: rgba(56,189,248,0.15) !important;
                border-color: rgba(56,189,248,0.42) !important;
                transform: translateX(3px);
            }

            section[data-testid="stSidebar"] div[role="radiogroup"] label p {
                font-size: .98rem !important;
                font-weight: 760 !important;
                color: #F8FAFC !important;
            }

            section[data-testid="stSidebar"] hr {
                border-color: rgba(148,197,253,0.20) !important;
                margin: 1.4rem 0;
            }

            /* Hero */
            .fid-hero {
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                gap: 24px;
                background:
                    radial-gradient(circle at 90% 24%, rgba(56,189,248,.25), transparent 28%),
                    linear-gradient(135deg, rgba(15,36,56,0.98), rgba(13,60,102,0.95));
                border: 1px solid rgba(148,197,253,0.26);
                border-radius: 30px;
                padding: 30px 34px;
                box-shadow: var(--fid-shadow);
                margin-bottom: 26px;
                color: var(--fid-text);
            }

            .fid-hero::after {
                content: "";
                position: absolute;
                width: 270px;
                height: 270px;
                right: -95px;
                top: -120px;
                background: rgba(56,189,248,0.13);
                border-radius: 50%;
            }

            .fid-hero-logo {
                position: relative;
                z-index: 1;
                width: 86px;
                height: 86px;
                min-width: 86px;
                border-radius: 26px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #38BDF8, #2563EB);
                color: #FFFFFF;
                font-size: 1.85rem !important;
                font-weight: 950;
                letter-spacing: -0.08em;
                border: 1px solid rgba(255,255,255,0.32);
                box-shadow: 0 20px 40px rgba(37,99,235,0.28);
            }

            .fid-hero-content {
                position: relative;
                z-index: 1;
            }

            .fid-kicker {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 7px 13px;
                border-radius: 999px;
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.17);
                color: #D9F1FF !important;
                font-size: .90rem !important;
                font-weight: 760;
                margin-bottom: 12px;
            }

            .fid-title {
                font-size: 2.95rem !important;
                font-weight: 950 !important;
                line-height: .98;
                letter-spacing: -0.065em;
                margin: 0 0 10px 0;
                color: #FFFFFF !important;
            }

            .fid-subtitle {
                font-size: 1.13rem !important;
                color: #C9D6E8 !important;
                max-width: 930px;
                line-height: 1.55;
                margin: 0;
            }

            /* Cards */
            .fid-card,
            .report-card,
            .quick-card,
            div[data-testid="stForm"] {
                background: var(--fid-card) !important;
                border: 1px solid var(--fid-border) !important;
                border-radius: 26px !important;
                box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22) !important;
            }

            .fid-card {
                padding: 25px 27px;
                margin-bottom: 22px;
            }

            .fid-card h3,
            .report-card h3 {
                color: var(--fid-text) !important;
                margin: 0 0 10px 0;
                font-size: 1.42rem !important;
                font-weight: 900 !important;
                letter-spacing: -0.035em;
            }

            .fid-card p,
            .report-card p {
                color: var(--fid-muted) !important;
                margin: 0;
                line-height: 1.62;
                font-size: 1.04rem !important;
            }

            .fid-section-title {
                font-size: 1.55rem !important;
                font-weight: 920 !important;
                color: var(--fid-text) !important;
                margin: 14px 0 8px 0;
                letter-spacing: -0.045em;
            }

            .fid-section-subtitle {
                color: var(--fid-muted) !important;
                font-size: 1.02rem !important;
                margin: -2px 0 18px 0;
            }

            .metric-card {
                position: relative;
                overflow: hidden;
                background:
                    radial-gradient(circle at 88% 8%, rgba(56,189,248,0.17), transparent 33%),
                    linear-gradient(135deg, rgba(15,36,56,0.98), rgba(19,46,72,0.98));
                padding: 25px 24px;
                border-radius: 26px;
                border: 1px solid rgba(148,197,253,0.22);
                box-shadow: 0 18px 42px rgba(0,0,0,0.22);
                margin-bottom: 18px;
                min-height: 145px;
            }

            .metric-icon {
                width: 52px;
                height: 52px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 18px;
                background: rgba(56,189,248,0.16);
                border: 1px solid rgba(56,189,248,0.23);
                font-size: 1.5rem !important;
                margin-bottom: 15px;
            }

            .metric-title {
                color: #BDD4EC !important;
                font-size: 1rem !important;
                font-weight: 770 !important;
                margin-bottom: 8px;
            }

            .metric-value {
                color: #FFFFFF !important;
                font-size: 2.45rem !important;
                font-weight: 950 !important;
                letter-spacing: -0.055em;
                line-height: 1;
            }

            .quick-card {
                padding: 22px;
                min-height: 134px;
                margin-bottom: 14px;
            }

            .quick-card-title {
                color: var(--fid-text) !important;
                font-size: 1.12rem !important;
                font-weight: 880 !important;
                margin-bottom: 8px;
            }

            .quick-card-text {
                color: var(--fid-muted) !important;
                font-size: 1rem !important;
                line-height: 1.52;
            }

            .report-card {
                padding: 22px 24px;
                margin-bottom: 20px;
            }

            .report-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 14px;
                margin: 14px 0 16px 0;
            }

            .report-mini {
                background: rgba(255,255,255,0.055);
                border: 1px solid rgba(148,197,253,0.16);
                border-radius: 18px;
                padding: 16px;
            }

            .report-mini-label {
                color: #9FB8D6 !important;
                font-size: .9rem !important;
                font-weight: 780;
                margin-bottom: 6px;
            }

            .report-mini-value {
                color: #FFFFFF !important;
                font-size: 1.18rem !important;
                font-weight: 880;
            }

            /* Native Streamlit elements */
            div[data-testid="stForm"] {
                padding: 23px 25px 25px 25px !important;
                margin-bottom: 22px;
            }

            label,
            div[data-testid="stForm"] label,
            div[data-testid="stTextInput"] label,
            div[data-testid="stTextArea"] label,
            div[data-testid="stSelectbox"] label,
            div[data-testid="stNumberInput"] label,
            div[data-testid="stDateInput"] label {
                font-weight: 780 !important;
                color: #EAF6FF !important;
                font-size: 1rem !important;
            }

            .stTextInput input,
            .stTextArea textarea,
            .stNumberInput input,
            div[data-baseweb="select"] > div {
                border-radius: 15px !important;
                border: 1px solid rgba(148,197,253,0.25) !important;
                background-color: #0C1F33 !important;
                color: #F8FAFC !important;
                min-height: 46px !important;
                font-size: 1rem !important;
            }

            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {
                color: #86A3C3 !important;
                opacity: 1 !important;
            }

            div[data-baseweb="select"] span,
            div[data-baseweb="select"] div {
                color: #F8FAFC !important;
                font-size: 1rem !important;
            }

            .stButton > button,
            .stDownloadButton > button,
            div[data-testid="stFormSubmitButton"] button {
                border-radius: 16px !important;
                border: 1px solid rgba(255,255,255,0.12) !important;
                background: linear-gradient(135deg, #38BDF8 0%, #2563EB 100%) !important;
                color: #FFFFFF !important;
                font-weight: 850 !important;
                font-size: 1rem !important;
                padding: .74rem 1.1rem !important;
                box-shadow: 0 12px 26px rgba(37,99,235,0.28);
                min-height: 46px;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover,
            div[data-testid="stFormSubmitButton"] button:hover {
                transform: translateY(-1px);
                box-shadow: 0 15px 30px rgba(56,189,248,0.30);
                border-color: rgba(255,255,255,0.24) !important;
            }

            [data-testid="stDataFrame"],
            [data-testid="stTable"] {
                border-radius: 20px !important;
                overflow: hidden !important;
                border: 1px solid rgba(148,197,253,0.18) !important;
                box-shadow: 0 18px 42px rgba(0,0,0,0.18) !important;
            }

            [data-testid="stDataFrame"] div,
            [data-testid="stDataFrame"] span {
                font-size: .96rem !important;
            }

            div[data-testid="stAlert"] {
                border-radius: 18px !important;
                border: 1px solid rgba(148,197,253,0.20) !important;
                font-size: 1rem !important;
            }

            .stInfo, .stSuccess, .stWarning, .stError {
                font-size: 1rem !important;
            }

            hr {
                margin: 1.35rem 0;
                border-color: rgba(148,197,253,0.18) !important;
            }

            /* Login */
            .login-intro {
                text-align: center;
                margin: 8px 0 18px 0;
            }

            .login-title {
                color: var(--fid-text) !important;
                font-size: 1.75rem !important;
                font-weight: 950 !important;
                margin-bottom: 7px;
                letter-spacing: -0.045em;
            }

            .login-subtitle {
                color: var(--fid-muted) !important;
                font-size: 1.03rem !important;
                line-height: 1.5;
            }

            @media (max-width: 900px) {
                html, body, [class*="css"] {
                    font-size: 16px !important;
                }
                .fid-hero {
                    display: block;
                    padding: 24px;
                    border-radius: 24px;
                }
                .fid-hero-logo {
                    width: 72px;
                    height: 72px;
                    min-width: 72px;
                    margin-bottom: 16px;
                }
                .fid-title {
                    font-size: 2.15rem !important;
                }
                .report-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def encabezado_principal(
    titulo="EvalúaFID",
    subtitulo="Sistema de evaluación formativa y gestión de evidencias para la Formación Inicial Docente",
    icono="📘",
    etiqueta="Plataforma académica",
):
    st.markdown(
        f"""
        <div class="fid-hero">
            <div class="fid-hero-logo">EF</div>
            <div class="fid-hero-content">
                <div class="fid-kicker">{icono} {etiqueta}</div>
                <div class="fid-title">{titulo}</div>
                <p class="fid-subtitle">{subtitulo}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tarjeta_metrica(titulo, valor, emoji):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{emoji}</div>
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tarjeta_bienvenida():
    st.markdown(
        """
        <div class="fid-card">
            <h3>Bienvenido a EvalúaFID</h3>
            <p>
                Panel académico para registrar cursos, estudiantes, criterios, rúbricas,
                evidencias, retroalimentaciones y reportes. La interfaz está optimizada para
                lectura amplia, navegación clara y trabajo institucional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def titulo_seccion(titulo, subtitulo=None):
    st.markdown(f'<div class="fid-section-title">{titulo}</div>', unsafe_allow_html=True)
    if subtitulo:
        st.markdown(f'<div class="fid-section-subtitle">{subtitulo}</div>', unsafe_allow_html=True)


def tarjeta_rapida(titulo, texto):
    st.markdown(
        f"""
        <div class="quick-card">
            <div class="quick-card-title">{titulo}</div>
            <div class="quick-card-text">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def tarjeta_reporte(curso, estudiante, total):
    st.markdown(
        f"""
        <div class="report-card">
            <h3>Resumen del reporte</h3>
            <div class="report-grid">
                <div class="report-mini">
                    <div class="report-mini-label">Curso</div>
                    <div class="report-mini-value">{curso}</div>
                </div>
                <div class="report-mini">
                    <div class="report-mini-label">Estudiante</div>
                    <div class="report-mini-value">{estudiante}</div>
                </div>
                <div class="report-mini">
                    <div class="report-mini-label">Registros</div>
                    <div class="report-mini-value">{total}</div>
                </div>
            </div>
            <p>Revisa el detalle de evidencias, criterios, niveles, puntajes y recomendaciones de mejora.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
