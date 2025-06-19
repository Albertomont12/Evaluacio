from typing import List, Dict, Tuple, Optional

# Datos (puedes dejar igual, pero modularizaremos el código)
alumnos = [
    {'id': 1, 'nombre': 'Juan', 'apellido_paterno': 'Perez', 'apellido_materno': 'Lopez'},
    {'id': 2, 'nombre': 'Maria', 'apellido_paterno': 'Lopez', 'apellido_materno': 'Garcia'},
    {'id': 3, 'nombre': 'Carlos', 'apellido_paterno': 'Gomez', 'apellido_materno': 'Martinez'},
]

asignaturas = [
    {'id': 1, 'nombre': 'Matematicas'},
    {'id': 2, 'nombre': 'Historia'},
    {'id': 3, 'nombre': 'Quimica'},
    {'id': 4, 'nombre': 'Literatura'},
    {'id': 5, 'nombre': 'Fisica'},
]

calificaciones = {
    (1, 1): [85, 90, 78],
    (1, 2): [70, 75, 80],
    (1, 3): [80, 82, 85],
    (1, 4): [90, 88, 92],
    (1, 5): [60, 65, 70],
    (2, 1): [88, 92, 95],
    (2, 2): [60, 65, 70],
    (2, 3): [85, 87, 90],
    (2, 4): [75, 80, 78],
    (2, 5): [82, 85, 88],
    (3, 1): [70, 72, 68],
    (3, 2): [85, 80, 90],
    (3, 3): [90, 95, 92],
    (3, 4): [60, 65, 58],
    (3, 5): [88, 90, 85],
}

COSTO_PARCIAL = 200
COSTO_SEMESTRAL = 350

def calcular_promedio(notas: List[int]) -> float:
    """Calcula el promedio de una lista de notas, redondeado a 1 decimal."""
    if not notas:
        return 0.0
    return round(sum(notas) / len(notas), 1)

def obtener_competencia(promedio: float) -> str:
    """Devuelve el acrónimo de competencia según promedio."""
    if promedio >= 90:
        return "EX"
    elif promedio >= 80:
        return "MB"
    elif promedio >= 70:
        return "B"
    elif promedio >= 60:
        return "R"
    else:
        return "SR"

def obtener_nombre_completo(alumno: Dict) -> str:
    """Concatena nombre completo de alumno."""
    return f"{alumno['nombre']} {alumno['apellido_paterno']} {alumno['apellido_materno']}"

def calcular_competencias() -> List[Dict]:
    """Calcula competencias por alumno y asignatura."""
    competencias = []
    for alumno in sorted(alumnos, key=lambda x: x['apellido_paterno']):
        for asignatura in asignaturas:
            key = (alumno['id'], asignatura['id'])
            notas = calificaciones.get(key)
            if notas:
                promedio = calcular_promedio(notas)
                competencia = obtener_competencia(promedio)
                competencias.append({
                    'alumno_id': alumno['id'],
                    'alumno_nombre': obtener_nombre_completo(alumno),
                    'asignatura_id': asignatura['id'],
                    'asignatura_nombre': asignatura['nombre'],
                    'promedio': promedio,
                    'competencia': competencia,
                })
    return competencias

def calcular_promedios_asignatura() -> Dict[int, float]:
    """Calcula promedio general por asignatura."""
    promedios = {}
    for asignatura in asignaturas:
        sumas = 0
        cuenta = 0
        for alumno in alumnos:
            key = (alumno['id'], asignatura['id'])
            notas = calificaciones.get(key)
            if notas:
                sumas += calcular_promedio(notas)
                cuenta += 1
        promedios[asignatura['id']] = round(sumas / cuenta, 1) if cuenta else 0.0
    return promedios

def calcular_indicadores() -> List[Dict]:
    """Calcula exámenes semestrales y parciales por alumno según reglas."""
    indicadores = []
    for alumno in alumnos:
        exa_semestral = 0
        exa_parcial = 0
        for asignatura in asignaturas:
            key = (alumno['id'], asignatura['id'])
            notas = calificaciones.get(key, [])
            if notas:
                promedio = calcular_promedio(notas)
                unidades_reprobadas = sum(1 for n in notas if n < 80)
                if promedio < 80:
                    exa_semestral += 1
                elif unidades_reprobadas > 0:
                    exa_parcial += unidades_reprobadas
        indicadores.append({
            'alumno_id': alumno['id'],
            'alumno_nombre': obtener_nombre_completo(alumno),
            'examenes_semestrales': exa_semestral,
            'examenes_parciales': exa_parcial,
        })
    return indicadores

def calcular_ingresos(indicadores: List[Dict]) -> List[Dict]:
    """Calcula pagos por alumno según exámenes."""
    ingresos = []
    for indicador in indicadores:
        pago_parciales = indicador['examenes_parciales'] * COSTO_PARCIAL
        pago_semestrales = indicador['examenes_semestrales'] * COSTO_SEMESTRAL
        pago_total = pago_parciales + pago_semestrales
        ingresos.append({
            'alumno_id': indicador['alumno_id'],
            'alumno_nombre': indicador['alumno_nombre'],
            'pago_parciales': pago_parciales,
            'pago_semestrales': pago_semestrales,
            'pago_total': pago_total,
        })
    return ingresos

def mostrar_competencias(competencias: List[Dict]) -> None:
    """Muestra el listado de competencias ordenado por apellido paterno."""
    print(f"{'Alumno':25} | {'Asignatura':12} | {'Promedio':8} | {'Competencia':11}")
    print("-"*65)
    for c in competencias:
        print(f"{c['alumno_nombre']:25} | {c['asignatura_nombre']:12} | {c['promedio']:8.1f} | {c['competencia']:11}")

def mostrar_promedios_asignatura(promedios: Dict[int, float]) -> None:
    """Muestra promedio general por asignatura."""
    print(f"\n{'Asignatura':12} | {'Promedio General':16}")
    print("-"*32)
    for asignatura in asignaturas:
        prom = promedios.get(asignatura['id'], 0.0)
        print(f"{asignatura['nombre']:12} | {prom:16.1f}")

def mostrar_indicadores(indicadores: List[Dict]) -> None:
    """Muestra exámenes a presentar por alumno."""
    print(f"\n{'Alumno':25} | {'Exámenes Semestrales':20} | {'Exámenes Parciales':18}")
    print("-"*70)
    for i in indicadores:
        print(f"{i['alumno_nombre']:25} | {i['examenes_semestrales']:20} | {i['examenes_parciales']:18}")

def mostrar_ingresos(ingresos: List[Dict]) -> None:
    """Muestra pagos por alumno."""
    print(f"\n{'Alumno':25} | {'Pago Parciales':15} | {'Pago Semestrales':17} | {'Pago Total':10}")
    print("-"*75)
    for i in ingresos:
        print(f"{i['alumno_nombre']:25} | ${i['pago_parciales']:14} | ${i['pago_semestrales']:16} | ${i['pago_total']:9}")

def menu():
    """Menú simple para elegir qué mostrar."""
    competencias = calcular_competencias()
    promedios_asignatura = calcular_promedios_asignatura()
    indicadores = calcular_indicadores()
    ingresos = calcular_ingresos(indicadores)

    while True:
        print("\nSistema de Gestión Escolar - Menú")
        print("1. Mostrar competencias por alumno y asignatura")
        print("2. Mostrar promedio general por asignatura")
        print("3. Mostrar indicadores de rendimiento")
        print("4. Mostrar ingresos por alumno")
        print("5. Salir")
        opcion = input("Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            mostrar_competencias(competencias)
        elif opcion == "2":
            mostrar_promedios_asignatura(promedios_asignatura)
        elif opcion == "3":
            mostrar_indicadores(indicadores)
        elif opcion == "4":
            mostrar_ingresos(ingresos)
        elif opcion == "5":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
