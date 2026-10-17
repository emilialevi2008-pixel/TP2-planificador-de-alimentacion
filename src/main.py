def main():
    print("======================================")
    print(" PLANIFICADOR DE ALIMENTACION SEMANAL")
    print("======================================")

    print("Bienvenido al planificador de comidas.")

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

if __name__ == "__main__":
    main()
