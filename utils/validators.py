def campo_vacio(valor: str) -> bool:
    return valor is None or str(valor).strip() == ""

def validar_curso(nombre_curso, programa_estudios, ciclo, periodo_academico, seccion):
    if campo_vacio(nombre_curso):
        return False, "El nombre del curso es obligatorio."
    if campo_vacio(programa_estudios):
        return False, "El programa de estudios es obligatorio."
    if campo_vacio(ciclo):
        return False, "El ciclo es obligatorio."
    if campo_vacio(periodo_academico):
        return False, "El periodo académico es obligatorio."
    if campo_vacio(seccion):
        return False, "La sección es obligatoria."
    return True, "Validación correcta."

def validar_estudiante(nombres, apellidos, codigo_estudiante, dni, id_curso):
    if campo_vacio(nombres):
        return False, "Los nombres son obligatorios."
    if campo_vacio(apellidos):
        return False, "Los apellidos son obligatorios."
    if campo_vacio(codigo_estudiante) and campo_vacio(dni):
        return False, "Debes registrar al menos código o DNI."
    if not id_curso:
        return False, "Debes asignar un curso."
    return True, "Validación correcta."