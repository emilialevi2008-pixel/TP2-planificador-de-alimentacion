import json
from pathlib import Path


def cargar_recetas():
    ruta = Path(__file__).resolve().parent.parent / "data" / "recetas.json"

    with open(ruta, "r", encoding="utf-8") as archivo:
        recetas = json.load(archivo)

    return recetas
def generar_menu_semanal(recetas, comidas_seleccionadas,ingredientes_excluidos, tiempo_maximo, metas_nutricionales):
    dias = [
        "Lunes", "Martes", "Miercoles",
        "Jueves", "Viernes", "Sabado", "Domingo"
    ]

    menu = {}

    for dia in dias:
        menu[dia] = {}
        nutrientes_acumulados = {
            "calorias": 0,
            "proteinas": 0,
            "carbohidratos": 0,
            "grasas": 0
        }
        print(f"\n===== {dia.upper()} =====")

        for comida in comidas_seleccionadas:
            recetas_disponibles = [
                receta for receta in recetas
                if receta["tipo"] == comida
                and receta["tiempo_minutos"] <= tiempo_maximo
                and not any(
                    excluido.lower() in ingrediente["nombre"].lower()
                    for ingrediente in receta["ingredientes"]
                    for excluido in ingredientes_excluidos
                )
            ]
            if metas_nutricionales:
                def calcular_distancia(receta):
                    distancia = 0

                    for nutriente, meta in metas_nutricionales.items():
                        total_estimado = (
                            nutrientes_acumulados[nutriente]
                            + receta[nutriente]
                        )

                        distancia += abs(meta - total_estimado) / meta

                    return distancia

                recetas_disponibles.sort(key=calcular_distancia)
            if not recetas_disponibles:
                print(f"No hay recetas disponibles para {comida}.")
                continue

            print(f"\nElegí tu {comida.lower()}:")

            for numero, receta in enumerate(recetas_disponibles, start=1):
                recomendacion = " [RECOMENDADA]" if metas_nutricionales and numero == 1 else ""
                print(
                    f"{numero}. {receta['nombre']}{recomendacion} | "
                    f"Tiempo: {receta['tiempo_minutos']} min | "
                    f"Costo: ${receta['costo_estimado']} | "
                    f"Calorias: {receta['calorias']} kcal | "
                    f"Proteinas: {receta['proteinas']} g"
                )
            while True:
                opcion = input("Ingresa el numero de la receta: ")

                if opcion.isdigit():
                    indice = int(opcion) - 1

                    if 0 <= indice < len(recetas_disponibles):
                        receta_elegida = recetas_disponibles[indice]
                        menu[dia][comida] = receta_elegida
                        for nutriente in nutrientes_acumulados:
                            nutrientes_acumulados[nutriente] += receta_elegida[nutriente]
                        break

                print("Opcion invalida. Intenta nuevamente.")

    return menu
def modificar_menu(menu_semanal, recetas, ingredientes_excluidos, tiempo_maximo):
    while True:
        print("\n===== MODIFICAR MENU =====")
        print("Dias disponibles:")

        dias = list(menu_semanal.keys())

        for numero, dia in enumerate(dias, start=1):
            print(f"{numero}. {dia}")

        print("0. Finalizar modificaciones")

        opcion_dia = input("Elegi un dia: ").strip()

        if opcion_dia == "0":
            break

        if not opcion_dia.isdigit() or not 1 <= int(opcion_dia) <= len(dias):
            print("Dia invalido.")
            continue

        dia = dias[int(opcion_dia) - 1]
        comidas = list(menu_semanal[dia].keys())

        if not comidas:
            print("No hay comidas para modificar ese dia.")
            continue

        print(f"\nComidas del {dia}:")

        for numero, comida in enumerate(comidas, start=1):
            print(f"{numero}. {comida}")

        opcion_comida = input("Elegi una comida: ").strip()

        if not opcion_comida.isdigit() or not 1 <= int(opcion_comida) <= len(comidas):
            print("Comida invalida.")
            continue

        comida = comidas[int(opcion_comida) - 1]

        disponibles = [
            receta for receta in recetas
            if receta["tipo"] == comida
            and receta["tiempo_minutos"] <= tiempo_maximo
            and not any(
                excluido in ingrediente["nombre"].lower()
                for ingrediente in receta["ingredientes"]
                for excluido in ingredientes_excluidos
            )
        ]

        if not disponibles:
            print("No hay recetas disponibles para esta comida.")
            continue

        print("\nRecetas disponibles:")

        for numero, receta in enumerate(disponibles, start=1):
            print(f"{numero}. {receta['nombre']}")

        opcion_receta = input("Elegi la nueva receta: ").strip()

        if not opcion_receta.isdigit() or not 1 <= int(opcion_receta) <= len(disponibles):
            print("Receta invalida.")
            continue

        receta_elegida = disponibles[int(opcion_receta) - 1]
        menu_semanal[dia][comida] = receta_elegida

        print(f"Receta actualizada: {receta_elegida['nombre']}")

    return menu_semanal


def calcular_costo_semanal(menu_semanal, cantidad_personas):
    costo_total = 0

    for dia, comidas in menu_semanal.items():
        for tipo, receta in comidas.items():
            costo_total += receta["costo_estimado"] * cantidad_personas

    return costo_total
def generar_lista_compras(menu_semanal, cantidad_personas):
    lista_compras = {}

    for dia, comidas in menu_semanal.items():
        for tipo, receta in comidas.items():
            for ingrediente in receta["ingredientes"]:
                nombre = ingrediente["nombre"].strip().lower()
                unidad = ingrediente["unidad"]
                cantidad = ingrediente["cantidad"] * cantidad_personas

                clave = (nombre, unidad)

                if clave in lista_compras:
                    lista_compras[clave] += cantidad
                else:
                    lista_compras[clave] = cantidad

    return lista_compras
def calcular_nutricion_diaria(menu_semanal):
    resultados = {}

    for dia, comidas in menu_semanal.items():
        totales = {
            "calorias": 0,
            "proteinas": 0,
            "carbohidratos": 0,
            "grasas": 0
        }

        for tipo, receta in comidas.items():
            for nutriente in totales:
                totales[nutriente] += receta[nutriente]

        resultados[dia] = totales
    return resultados
def main():
    print("\n===== OBJETIVO NUTRICIONAL =====")

    while True:
        print("¿Queres establecer un objetivo nutricional?")
        print("1. Si")
        print("2. No")

        opcion_objetivo = input("Elegi una opcion: ").strip()

        if opcion_objetivo in ("1", "2"):
            break

        print("Opcion invalida. Ingresa 1 o 2.")

    metas_nutricionales = {}

    if opcion_objetivo == "1":
        print("\n===== TUS METAS NUTRICIONALES DIARIAS =====")

        nutrientes = {
            "calorias": "Calorias (kcal)",
            "proteinas": "Proteinas (g)",
            "carbohidratos": "Carbohidratos (g)",
            "grasas": "Grasas (g)"
        }

        for nutriente, descripcion in nutrientes.items():
            while True:
                entrada = input(
                    f"Objetivo diario de {descripcion} (Enter para omitir): "
                ).strip()

                if entrada == "":
                    break

                try:
                    valor = float(entrada.replace(",", "."))

                    if valor > 0:
                        metas_nutricionales[nutriente] = valor
                        break

                except ValueError:
                    pass

                print("Ingresa un numero mayor que cero o presiona Enter.")
    print("======================================")
    print(" PLANIFICADOR DE ALIMENTACION SEMANAL")
    print("======================================")

    print("Bienvenido al planificador de comidas.")

    recetas = cargar_recetas()

    print(f"Recetas disponibles: {len(recetas)}")

    while True:
        entrada = input("¿Para cuantas personas es el menu? ").strip()

        if entrada.isdigit() and int(entrada) > 0:
            cantidad_personas = int(entrada)
            break

        print("Error: ingresa un numero entero mayor que cero.")
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

    while True:
        entrada = input("Ingresa tu presupuesto semanal: ").strip()

        try:
            presupuesto = float(entrada.replace(",", "."))

            if presupuesto >= 0:
                break

        except ValueError:
            pass

        print("Error: ingresa un presupuesto valido, mayor o igual a cero.")
    print(f"Tu presupuesto semanal es de ${presupuesto:,.2f}")

    print("\nINGREDIENTES EXCLUIDOS")

    respuesta = input(
        "¿Que ingredientes queres excluir? "
        "(separados por comas, o Enter para ninguno): "
    )

    ingredientes_excluidos = [
        ingrediente.strip().lower()
        for ingrediente in respuesta.split(",")
        if ingrediente.strip()
    ]
    print("\nTIEMPO MAXIMO DE PREPARACION")

    while True:
        entrada = input("Ingresa el tiempo maximo de preparacion en minutos: ").strip()

        if entrada.isdigit() and int(entrada) > 0:
            tiempo_maximo = int(entrada)
            break

        print("Error: ingresa un numero entero mayor que cero.")
    menu_semanal = generar_menu_semanal(
        recetas, comidas_seleccionadas, ingredientes_excluidos, tiempo_maximo, metas_nutricionales
    )

    print("\n¿Queres modificar alguna receta del menu?")
    respuesta_modificar = input("Escribi si o no: ").strip().lower()

    if respuesta_modificar in ("si", "sí", "s"):
        menu_semanal = modificar_menu(
            menu_semanal,
            recetas,
            ingredientes_excluidos,
            tiempo_maximo
        )
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

    lista_compras = generar_lista_compras(
        menu_semanal, cantidad_personas
    )

    print("\n===== LISTA DE COMPRAS SEMANAL =====")

    for (nombre, unidad), cantidad in sorted(lista_compras.items()):
        print(f"- {nombre}: {cantidad:g} {unidad}")
    nutricion_diaria = calcular_nutricion_diaria(menu_semanal)

    print("\n===== INFORMACION NUTRICIONAL POR DIA =====")

    for dia, comidas in menu_semanal.items():
        print(f"\n========== {dia.upper()} ==========")

        for tipo, receta in comidas.items():
            print(f"\n{tipo.upper()}: {receta['nombre']}")
            print(f"Calorias: {receta['calorias']:,.0f} kcal")
            print(f"Proteinas: {receta['proteinas']:,.1f} g")
            print(f"Carbohidratos: {receta['carbohidratos']:,.1f} g")
            print(f"Grasas: {receta['grasas']:,.1f} g")

        total = nutricion_diaria[dia]

        print(f"\nTOTAL DEL {dia.upper()}")
        print(f"Calorias: {total['calorias']:,.0f} kcal")
        print(f"Proteinas: {total['proteinas']:,.1f} g")
        print(f"Carbohidratos: {total['carbohidratos']:,.1f} g")
        print(f"Grasas: {total['grasas']:,.1f} g")
        if metas_nutricionales:
            print(f"\n===== OBJETIVOS NUTRICIONALES DEL {dia.upper()} =====")

            nombres = {
                "calorias": "Calorias",
                "proteinas": "Proteinas",
                "carbohidratos": "Carbohidratos",
                "grasas": "Grasas"
            }

            for nutriente, meta in metas_nutricionales.items():
                consumido = total[nutriente]
                diferencia = meta - consumido
                unidad = "kcal" if nutriente == "calorias" else "g"

                print(f"\n{nombres[nutriente]}:")
                print(f"Total del menu: {consumido:.1f} {unidad}")
                print(f"Objetivo diario: {meta:.1f} {unidad}")

                if abs(diferencia) < 0.01:
                    print("Objetivo alcanzado.")
                elif diferencia > 0:
                    print(f"Faltan {diferencia:.1f} {unidad} para alcanzar el objetivo.")
                else:
                    print(f"Superaste el objetivo por {abs(diferencia):.1f} {unidad}.")
if __name__ == "__main__":
    main()
