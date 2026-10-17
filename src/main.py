import json
from pathlib import Path


def cargar_recetas():
    ruta = Path(__file__).resolve().parent.parent / "data" / "recetas.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        recetas = json.load(archivo)

    return recetas
def generar_menu_semanal(recetas, comidas_seleccionadas):
    dias = [
        "Lunes", "Martes", "Miercoles",
        "Jueves", "Viernes", "Sabado", "Domingo"
    ]

    menu = {}

    for dia in dias:
        menu[dia] = {}
        print(f"\n===== {dia.upper()} =====")

        for comida in comidas_seleccionadas:
            recetas_disponibles = [
                receta for receta in recetas
                if receta["tipo"] == comida
            ]

            if not recetas_disponibles:
                print(f"No hay recetas disponibles para {comida}.")
                continue

            print(f"\nElegí tu {comida.lower()}:")

            for numero, receta in enumerate(recetas_disponibles, start=1):
                print(f"{numero}. {receta['nombre']}")

            while True:
                opcion = input("Ingresa el numero de la receta: ")

                if opcion.isdigit():
                    indice = int(opcion) - 1

                    if 0 <= indice < len(recetas_disponibles):
                        receta_elegida = recetas_disponibles[indice]
                        menu[dia][comida] = receta_elegida
                        break

                print("Opcion invalida. Intenta nuevamente.")

    return menu



def calcular_costo_semanal(menu_semanal, cantidad_personas):
    costo_total = 0

    for dia, comidas in menu_semanal.items():
        for tipo, receta in comidas.items():
            costo_total += receta["costo_estimado"] * cantidad_personas

    return costo_total
def main():
    print("======================================")
    print(" PLANIFICADOR DE ALIMENTACION SEMANAL")
    print("======================================")

    print("Bienvenido al planificador de comidas.")

    recetas = cargar_recetas()

    print(f"Recetas disponibles: {len(recetas)}")

    cantidad_personas = int(
        input("¿Para cuantas personas queres planificar? ")
    )

    print(f"Vamos a planificar comidas para {cantidad_personas} personas.")

    print("\nSelecciona las comidas que queres incluir:")
    print("1. Desayuno")
    print("2. Almuerzo")
    print("3. Merienda")
    print("4. Cena")

    opciones = input(
        "Ingresa los numeros separados por comas (ejemplo: 1,2,3,4): "
    )

    tipos_comida = {
        "1": "Desayuno",
        "2": "Almuerzo",
        "3": "Merienda",
        "4": "Cena"
    }

    comidas_seleccionadas = []

    for opcion in opciones.split(","):
        opcion = opcion.strip()
        if opcion in tipos_comida:
            comida = tipos_comida[opcion]

            if comida not in comidas_seleccionadas:
                comidas_seleccionadas.append(comida)

    print("\nComidas seleccionadas:")

    for comida in comidas_seleccionadas:
        print(f"- {comida}")

    print("\nPRESUPUESTO SEMANAL")

    presupuesto = float(
        input("¿Cuanto dinero queres gastar por semana en pesos? ")
    )

    print(f"Tu presupuesto semanal es de ${presupuesto:,.2f}")

    menu_semanal = generar_menu_semanal(recetas, comidas_seleccionadas)

    print("\nMENU SEMANAL GENERADO")

    for dia, comidas in menu_semanal.items():
        print(f"\n{dia}:")

        for tipo, receta in comidas.items():
            print(f"  {tipo}: {receta['nombre']}")

    costo_total = calcular_costo_semanal(
        menu_semanal, cantidad_personas
    )

    print("\nRESUMEN DEL PRESUPUESTO")
    print(f"Costo total estimado: ${costo_total:,.2f}")
    print(f"Presupuesto disponible: ${presupuesto:,.2f}")

    diferencia = presupuesto - costo_total

    if diferencia >= 0:
        print(f"Dinero restante: ${diferencia:,.2f}")
    else:
        print(f"Presupuesto excedido por: ${abs(diferencia):,.2f}")
if __name__ == "__main__":
    main()
