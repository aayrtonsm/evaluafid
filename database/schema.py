import hashlib
from database.db import execute_query, fetch_one

def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

def crear_admin_inicial():
    usuario = fetch_one(
        "SELECT * FROM usuarios WHERE nombre_usuario = ?",
        ("admin",)
    )

    if not usuario:
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
                "admin",
                hash_clave("123456"),
                "Administrador",
                "Activo",
                "Administrador del sistema",
                "admin@evaluafid.local"
            )
        )

def create_tables():
    execute_query("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        clave_hash TEXT NOT NULL,
        rol TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Activo',
        nombre_completo TEXT,
        correo TEXT,
        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS configuracion (
        id_configuracion INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_institucion TEXT NOT NULL,
        periodo_actual TEXT,
        responsable_sistema TEXT,
        correo_contacto TEXT,
        logo_url TEXT,
        fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS cursos (
        id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_curso TEXT NOT NULL,
        programa_estudios TEXT NOT NULL,
        ciclo TEXT NOT NULL,
        periodo_academico TEXT NOT NULL,
        seccion TEXT NOT NULL,
        descripcion TEXT,
        docente_responsable TEXT,
        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
        estado TEXT DEFAULT 'Activo'
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_estudiante TEXT,
        dni TEXT,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        correo TEXT,
        telefono TEXT,
        id_curso INTEGER NOT NULL,
        observaciones TEXT,
        estado TEXT DEFAULT 'Activo',
        fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS criterios_evaluacion (
        id_criterio INTEGER PRIMARY KEY AUTOINCREMENT,
        id_curso INTEGER NOT NULL,
        competencia TEXT NOT NULL,
        criterio TEXT NOT NULL,
        descripcion TEXT,
        ponderacion REAL,
        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
        estado TEXT DEFAULT 'Activo',
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS rubricas (
        id_rubrica INTEGER PRIMARY KEY AUTOINCREMENT,
        id_curso INTEGER NOT NULL,
        id_criterio INTEGER NOT NULL,
        nombre_rubrica TEXT NOT NULL,
        descripcion TEXT,
        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
        estado TEXT DEFAULT 'Activo',
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
        FOREIGN KEY (id_criterio) REFERENCES criterios_evaluacion(id_criterio)
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS niveles_rubrica (
        id_nivel INTEGER PRIMARY KEY AUTOINCREMENT,
        id_rubrica INTEGER NOT NULL,
        nombre_nivel TEXT NOT NULL,
        descriptor TEXT,
        puntaje REAL,
        orden_nivel INTEGER,
        FOREIGN KEY (id_rubrica) REFERENCES rubricas(id_rubrica)
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS evidencias (
        id_evidencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estudiante INTEGER NOT NULL,
        id_curso INTEGER NOT NULL,
        id_criterio INTEGER NOT NULL,
        id_rubrica INTEGER,
        tipo_evidencia TEXT NOT NULL,
        nombre_evidencia TEXT NOT NULL,
        descripcion TEXT,
        fecha_entrega TEXT,
        estado_entrega TEXT,
        fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
        FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
        FOREIGN KEY (id_criterio) REFERENCES criterios_evaluacion(id_criterio),
        FOREIGN KEY (id_rubrica) REFERENCES rubricas(id_rubrica)
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS retroalimentaciones (
        id_retroalimentacion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_evidencia INTEGER NOT NULL,
        id_estudiante INTEGER NOT NULL,
        id_criterio INTEGER NOT NULL,
        id_nivel INTEGER NOT NULL,
        comentario_docente TEXT NOT NULL,
        recomendacion_mejora TEXT,
        fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_evidencia) REFERENCES evidencias(id_evidencia),
        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
        FOREIGN KEY (id_criterio) REFERENCES criterios_evaluacion(id_criterio),
        FOREIGN KEY (id_nivel) REFERENCES niveles_rubrica(id_nivel)
    )
    """)

    crear_admin_inicial()