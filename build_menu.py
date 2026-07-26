# -*- coding: utf-8 -*-
import json

CATS = {}

def ing(nombre, cantidad, unidad, categoria):
    if nombre in CATS and CATS[nombre] != categoria:
        raise ValueError(f"Categoria distinta para {nombre}: {CATS[nombre]} vs {categoria}")
    CATS[nombre] = categoria
    return {"nombre": nombre, "cantidad": cantidad, "unidad": unidad, "categoria": categoria}

def meal(titulo, base, extra_ruben=None, nota=""):
    return {"titulo": titulo, "base": base, "extra_ruben": extra_ruben or [], "nota": nota}

def almuerzo(lydia, ruben):
    return {"Lydia": lydia, "Ruben": ruben}

def paso(titulo, ingredientes, instrucciones):
    return {"titulo": titulo, "ingredientes": ingredientes, "instrucciones": instrucciones}

def suma_semana(semana, nombre):
    """Suma cuanto se usa de un ingrediente 'nombre' a lo largo de toda la semana
    (en todas las comidas, tanto en 'base' como en 'extra_ruben')."""
    total = 0.0
    unidad = "g"
    for comidas in semana["dias"].values():
        for comida in comidas.values():
            bloques = []
            if "Lydia" in comida or "Ruben" in comida:
                if "Lydia" in comida: bloques.append(comida["Lydia"])
                if "Ruben" in comida: bloques.append(comida["Ruben"])
            else:
                bloques.append(comida)
            for b in bloques:
                for it in (b.get("base") or []) + (b.get("extra_ruben") or []):
                    if it["nombre"] == nombre:
                        total += it["cantidad"]
                        unidad = it["unidad"]
    return total, unidad

def ing_total(semana, nombre, categoria):
    """Ingrediente cuya cantidad para el domingo se calcula sola, sumando lo que
    se usa de 'nombre' en las comidas de toda la semana (evita tener que cuadrar
    a mano la cantidad del cocinado grande con lo que luego se usa dia a dia).
    Se marca como 'derivado' para que la lista de la compra no lo cuente dos veces
    (una en el paso del domingo y otra en cada comida donde se usa)."""
    total, unidad = suma_semana(semana, nombre)
    cantidad = int(round(total)) if float(total).is_integer() or unidad == "ud" else round(total, 1)
    item = ing(nombre, cantidad, unidad, categoria)
    item["derivado"] = True
    return item

C_VERD = "Frescos: verdura y hortaliza"
C_FRUTA = "Fruta fresca"
C_CARNE = "Carne, aves y huevos"
C_PESCA = "Pescaderia"
C_LACTEO = "Lacteos (pasteurizados)"
C_CEREAL = "Despensa: cereales, pan y pasta"
C_LEGUM = "Despensa: legumbres y conservas"
C_FRUTOSEC = "Frutos secos y semillas"
C_SALSA = "Aceites, salsas y condimentos"
C_OTROS = "Otros"


# =========================================================================
# SEMANA A
# =========================================================================
SEMANA_A = {
  "nombre": "Semana A",
  "dias": {
    "Lunes": {
      "Desayuno": {
        "Lydia": meal("Tostada con aguacate y huevo a la plancha",
          [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
           ing("Aguacate", 50, "g", C_VERD),
           ing("Huevo campero (M)", 1, "ud", C_CARNE),
           ing("Kefir natural", 150, "g", C_LACTEO)],
          nota="Huevo a la plancha con una pizca de sal."),
        "Ruben": meal("Doble racion + platano (post-rodaje suave)",
          [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
           ing("Aguacate", 30, "g", C_VERD),
           ing("Huevo campero (M)", 1, "ud", C_CARNE),
           ing("Platano", 100, "g", C_FRUTA),
           ing("Nueces naturales", 20, "g", C_FRUTOSEC)],
          nota="Desayuna al volver de correr. Tostadas + aguacate + huevo iguales que Lydia, mas esta linea extra."),
      },
      "Almuerzo": almuerzo(
        meal("Batido de platano, avena y leche",
          [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
           ing("Copos de avena sin gluten", 20, "g", C_CEREAL)],
          nota="Batir todo junto (Thermomix o batidora)."),
        meal("Yogur, fruta y nueces",
          [ing("Yogur natural sin azucar", 250, "g", C_LACTEO), ing("Melocoton", 300, "g", C_FRUTA),
           ing("Nueces naturales", 40, "g", C_FRUTOSEC),
           ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
           ing("Creatina monohidrato", 5, "g", C_OTROS)])),
      "Comida": meal("Bowl tupper de pasta sin gluten, pollo, verduras asadas y hummus",
        [ing("Pasta sin gluten (fusilli maiz-arroz)", 105, "g", C_CEREAL),
         ing("Pechuga de pollo", 300, "g", C_CARNE),
         ing("Rucula", 60, "g", C_VERD),
         ing("Aceite de oliva virgen extra", 15, "g", C_SALSA)],
        extra_ruben=[ing("Pasta sin gluten (fusilli maiz-arroz)", 25, "g", C_CEREAL)],
        nota="Pasta sin gluten (45 g Lydia / 60 g Ruben aprox.) y pollo (cocinados el domingo) + 300 g de verduras asadas + 100 g de hummus (tambien del domingo) + rucula fresca + aceite. Se toma templado o frio, aguanta bien de un dia para otro."),
      "Merienda": meal("Tostada con crema de cacahuete y platano",
        [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
         ing("Crema de cacahuete 100%", 20, "g", C_FRUTOSEC),
         ing("Platano", 100, "g", C_FRUTA)],
        extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
                     ing("Crema de cacahuete 100%", 10, "g", C_FRUTOSEC)],
        nota="Antes de musculacion (Ruben) / antes del entreno de tarde (Lydia)."),
      "Cena": meal("Salmon al horno con ensalada de aguacate",
        [ing("Salmon (lomo fresco)", 200, "g", C_PESCA),
         ing("Tomate", 150, "g", C_VERD),
         ing("Apio", 80, "g", C_VERD),
         ing("Aguacate", 50, "g", C_VERD),
         ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
        extra_ruben=[ing("Boniato", 100, "g", C_VERD)],
        nota="Salmon ya cocinado el domingo, recalentar suave (airfryer 160C 3-4 min)."),
    },
  }
}
print("Semana A: Lunes OK")

SEMANA_A["dias"]["Martes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con aguacate y tomate",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Aguacate", 60, "g", C_VERD),
       ing("Tomate", 60, "g", C_VERD),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
      nota="Tomate en rodajas y aguacate aplastado con un chorrito de AOVE, sal y oregano."),
    "Ruben": meal("Porridge de avena con platano",
      [ing("Copos de avena sin gluten", 80, "g", C_CEREAL),
       ing("Leche desnatada", 250, "g", C_LACTEO),
       ing("Platano", 100, "g", C_FRUTA),
       ing("Canela", 1, "g", C_SALSA)],
      nota="Antes de nadar/bici (no hace falta ir en ayunas este dia). Microondas 2 min, remover."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa y leche",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fresa", 150, "g", C_FRUTA)],
      nota="Batir todo junto."),
    meal("Kefir, fruta y frutos secos",
      [ing("Kefir natural", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Almendras crudas", 30, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada templada de boniato, atun y huevo (tupper)",
    [ing("Boniato", 250, "g", C_VERD),
     ing("Atun al natural (lata)", 160, "g", C_LEGUM),
     ing("Judias verdes", 200, "g", C_VERD),
     ing("Aceitunas negras sin hueso", 40, "g", C_LEGUM),
     ing("Aceite de oliva virgen extra", 15, "g", C_SALSA),
     ing("Vinagre de manzana", 5, "g", C_SALSA)],
    extra_ruben=[ing("Boniato", 150, "g", C_VERD)],
    nota="Boniato asado (del domingo) + 2 latas de atun + huevo cocido (2, del domingo) + judias verdes cocidas + aceitunas + aliño. No lleva nada que se ponga malo con el calor."),
  "Merienda": meal("Yogur con nueces tostadas y miel",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO),
     ing("Miel", 10, "g", C_SALSA),
     ing("Nueces naturales", 20, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Nueces naturales", 15, "g", C_FRUTOSEC)],
    nota="Tostar las nueces 5 min en airfryer a 160C para que esten crujientes."),
  "Cena": meal("Tortilla francesa de espinacas con ensalada",
    [ing("Huevo campero (M)", 4, "ud", C_CARNE),
     ing("Espinacas frescas", 150, "g", C_VERD),
     ing("Lechuga", 60, "g", C_VERD),
     ing("Tomate", 80, "g", C_VERD),
     ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Huevo campero (M)", 2, "ud", C_CARNE),
                 ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 50, "g", C_CEREAL)],
    nota="Cena ligera. Ruben añade 2 huevos mas a la tortilla y pan sin gluten aparte."),
}

SEMANA_A["dias"]["Miercoles"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con hummus y tomate cherry",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Tomate cherry", 50, "g", C_VERD),
       ing("Semillas de sesamo", 5, "g", C_FRUTOSEC),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
      nota="60 g de hummus del domingo + tomate cherry laminado + sesamo por encima."),
    "Ruben": meal("Tostadas con huevo revuelto y aguacate (post-series)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Huevo campero (M)", 3, "ud", C_CARNE),
       ing("Aguacate", 50, "g", C_VERD),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
      nota="Dia de series: desayuno mas completo al volver a casa."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de platano y cacao",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
       ing("Cacao desgrasado en polvo sin azucar", 5, "g", C_OTROS)],
      nota="Batir todo junto."),
    meal("Fruta y yogur proteico",
      [ing("Yogur griego natural", 150, "g", C_LACTEO), ing("Sandia", 300, "g", C_FRUTA),
       ing("Almendras crudas", 20, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl de lomo de cerdo, arroz basmati y verduras asadas (tupper, estilo asiatico)",
    [ing("Arroz basmati", 105, "g", C_CEREAL),
     ing("Lomo de cerdo", 250, "g", C_CARNE),
     ing("Salsa de soja sin gluten (tamari)", 15, "g", C_SALSA),
     ing("Semillas de sesamo", 5, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Arroz basmati", 25, "g", C_CEREAL), ing("Lomo de cerdo", 50, "g", C_CARNE)],
    nota="Arroz basmati (45 g Lydia / 60 g Ruben aprox.) + lomo de cerdo + 250 g de verduras asadas (todo del domingo) salteado 2 min con tamari y sesamo, o en frio como bowl."),
  "Merienda": meal("Tostada con pavo casero desmenuzado",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
     ing("Pechuga de pavo (fresca, no fiambre)", 60, "g", C_CARNE),
     ing("Tomate", 40, "g", C_VERD)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
                 ing("Pechuga de pavo (fresca, no fiambre)", 40, "g", C_CARNE)],
    nota="Pavo cocinado a la plancha en casa (no fiambre envasado), se puede dejar hecho el domingo si se prefiere."),
  "Cena": meal("Salmorejo casero con huevo duro",
    [ing("Huevo campero (M)", 2, "ud", C_CARNE)],
    extra_ruben=[ing("Boniato", 150, "g", C_VERD)],
    nota="400 ml de salmorejo/gazpacho del domingo, bien frio, con huevo duro picado por encima. Perfecto para el calor de julio."),
}
print("Semana A: Martes y Miercoles OK")

SEMANA_A["dias"]["Jueves"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con crema de cacahuete y platano",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Crema de cacahuete 100%", 20, "g", C_FRUTOSEC),
       ing("Platano", 80, "g", C_FRUTA),
       ing("Canela", 1, "g", C_SALSA)],
      nota=""),
    "Ruben": meal("Tostadas con atun y tomate",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Atun al natural (lata)", 80, "g", C_LEGUM),
       ing("Tomate", 60, "g", C_VERD),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
      nota="Dia de bici/gimnasio, no corre en ayunas."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de frutos rojos, avena y leche",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fruta de temporada (variada)", 120, "g", C_FRUTA),
       ing("Copos de avena sin gluten", 20, "g", C_CEREAL)],
      nota="Batir todo junto."),
    meal("Kefir, fruta y nueces",
      [ing("Kefir natural", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Nueces naturales", 30, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl de atun a la plancha, arroz y aguacate (tupper)",
    [ing("Arroz basmati", 90, "g", C_CEREAL),
     ing("Atun fresco (lomo)", 200, "g", C_PESCA),
     ing("Aguacate", 100, "g", C_VERD),
     ing("Edamame (vaina o desgranado, congelado)", 100, "g", C_VERD),
     ing("Zanahoria", 60, "g", C_VERD),
     ing("Salsa de soja sin gluten (tamari)", 15, "g", C_SALSA),
     ing("Semillas de sesamo", 5, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Arroz basmati", 25, "g", C_CEREAL), ing("Atun fresco (lomo)", 50, "g", C_PESCA)],
    nota="Arroz basmati (40 g Lydia / 50 g Ruben aprox.) + atun fresco a la plancha del domingo (bien hecho por dentro, nada de crudo), en dados, con aguacate, edamame y zanahoria. Frio, ideal para tupper de verano."),
  "Merienda": meal("Yogur con fruta y almendras",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO),
     ing("Almendras crudas", 15, "g", C_FRUTOSEC),
     ing("Fruta de temporada (variada)", 100, "g", C_FRUTA)],
    extra_ruben=[ing("Almendras crudas", 10, "g", C_FRUTOSEC)]),
  "Cena": meal("Pollo al horno con verduras y patata",
    [ing("Pechuga de pollo", 200, "g", C_CARNE),
     ing("Pimiento rojo", 100, "g", C_VERD), ing("Cebolla", 80, "g", C_VERD),
     ing("Calabacin", 100, "g", C_VERD), ing("Patata", 150, "g", C_VERD),
     ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)],
    nota="Pollo restante del domingo, recalentado con verduras nuevas al horno 20 min a 200C."),
}

SEMANA_A["dias"]["Viernes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con huevo revuelto y espinacas",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE),
       ing("Espinacas frescas", 60, "g", C_VERD)],
      nota=""),
    "Ruben": meal("Tostadas con huevo, pavo y miel (post-tirada larga)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE),
       ing("Pechuga de pavo (fresca, no fiambre)", 60, "g", C_CARNE),
       ing("Platano", 100, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA)],
      nota="Tirada larga con tempo: desayuno mas calorico y con miel para reponer glucogeno."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de melocoton y leche",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Melocoton", 150, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA)],
      nota="Batir todo junto."),
    meal("Fruta y yogur",
      [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Nueces naturales", 15, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada de garbanzos con atun (tupper, dia de compra)",
    [ing("Garbanzos cocidos (bote o secos)", 300, "g", C_LEGUM),
     ing("Atun al natural (lata)", 160, "g", C_LEGUM),
     ing("Pimiento rojo", 100, "g", C_VERD), ing("Tomate", 100, "g", C_VERD),
     ing("Cebolla", 50, "g", C_VERD), ing("Aceite de oliva virgen extra", 15, "g", C_SALSA),
     ing("Vinagre de manzana", 5, "g", C_SALSA)],
    extra_ruben=[ing("Garbanzos cocidos (bote o secos)", 100, "g", C_LEGUM)],
    nota="Usar el hummus/garbanzos que sobren; si no queda, es la unica compra extra de garbanzos de la semana."),
  "Merienda": meal("Tostada con platano y miel + frutos secos",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
     ing("Platano", 80, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA),
     ing("Almendras crudas", 15, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
                 ing("Almendras crudas", 10, "g", C_FRUTOSEC)],
    nota="Antes de entrenar los dos (Lydia tarde, Ruben musculacion/gimnasio)."),
  "Cena": meal("Dorada al horno con verduras",
    [ing("Dorada o lubina (filete)", 350, "g", C_PESCA),
     ing("Calabacin", 150, "g", C_VERD), ing("Tomate", 100, "g", C_VERD),
     ing("Cebolla", 80, "g", C_VERD), ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)],
    nota="Cena ligera antes del fin de semana. Horno 20 min a 200C."),
}
print("Semana A: Jueves y Viernes OK")

SEMANA_A["dias"]["Sabado"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con queso fresco y fruta",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 80, "g", C_LACTEO),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
      nota="Tranquila, sin prisas."),
    "Ruben": meal("Avena con platano y miel (pre-ruta larga)",
      [ing("Copos de avena sin gluten", 90, "g", C_CEREAL),
       ing("Leche desnatada", 200, "g", C_LACTEO),
       ing("Platano", 100, "g", C_FRUTA), ing("Miel", 15, "g", C_SALSA)],
      nota="Desayuno con carga de hidratos antes de salir (minimo 2h30 de bici). Durante la ruta: platano/dátiles o gel cada 45-60 min, bidon con bebida isotonica o agua+sal+miel."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa y platano",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fresa", 100, "g", C_FRUTA), ing("Platano", 60, "g", C_FRUTA)],
      nota="Batir todo junto."),
    meal("Fruta y frutos secos",
      [ing("Fruta de temporada (variada)", 200, "g", C_FRUTA), ing("Almendras crudas", 15, "g", C_FRUTOSEC),
       ing("Platano", 100, "g", C_FRUTA)],
      nota="Si la ruta se alarga, tomar a media mañana en casa nada mas volver, con el batido de recuperacion de la merienda adelantado si hace falta.")),
  "Comida": meal("Comida libre de la semana",
    [], nota="Aprovechar el sabado para la comida libre (fuera de casa o lo que apetezca). No se detalla menu: es la comida flexible de la semana."),
  "Merienda": almuerzo(
    meal("Batido de platano y fresa",
      [ing("Leche desnatada", 200, "g", C_LACTEO), ing("Platano", 80, "g", C_FRUTA), ing("Fresa", 80, "g", C_FRUTA)],
      nota="A su hora habitual."),
    meal("Batido de recuperacion",
      [ing("Leche desnatada", 250, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 30, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)],
      nota="Nada mas terminar la ruta o al llegar a casa.")),
  "Cena": meal("Arroz cremoso con ternera y champiñones",
    [ing("Arroz basmati", 110, "g", C_CEREAL),
     ing("Ternera magra (tacos o filetes)", 200, "g", C_CARNE),
     ing("Champiñones", 200, "g", C_VERD), ing("Cebolla", 60, "g", C_VERD),
     ing("Queso mozzarella light pasteurizado", 60, "g", C_LACTEO),
     ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Arroz basmati", 30, "g", C_CEREAL), ing("Ternera magra (tacos o filetes)", 50, "g", C_CARNE)],
    nota="Arroz (50 g Lydia / 60 g Ruben aprox., es plato unico asi que algo mas generoso). Ternera comprada y cocinada fresca ese mismo dia (no es del cocinado del domingo). Pochar cebolla y champiñones, añadir la ternera troceada, el arroz y caldo/agua poco a poco removiendo tipo risotto unos 18-20 min; terminar con el queso rallado fuera del fuego. Cena de fin de semana, algo mas relajada."),
}

SEMANA_A["dias"]["Domingo"] = {
  "Desayuno": meal("Tortitas de avena y platano (pre-Hyrox)",
    [ing("Copos de avena sin gluten", 70, "g", C_CEREAL),
     ing("Platano", 180, "g", C_FRUTA), ing("Huevo campero (M)", 3, "ud", C_CARNE),
     ing("Canela", 1, "g", C_SALSA), ing("Miel", 10, "g", C_SALSA)],
    extra_ruben=[ing("Copos de avena sin gluten", 20, "g", C_CEREAL), ing("Huevo campero (M)", 1, "ud", C_CARNE)],
    nota="Triturar la avena, el platano y los huevos hasta obtener una masa fina; añadir la canela. Tortitas pequeñas en sarten antiadherente, 2-3 min por lado. Desayuno ligero antes del Hyrox de los dos, facil de digerir."),
  "Almuerzo": meal("Recuperacion post-Hyrox: huevos revueltos y tostada",
    [ing("Huevo campero (M)", 4, "ud", C_CARNE),
     ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
     ing("Fruta de temporada (variada)", 200, "g", C_FRUTA), ing("Kefir natural", 200, "g", C_LACTEO)],
    extra_ruben=[ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 40, "g", C_CEREAL)],
    nota="Nada mas llegar del box, antes de poneros con el cocinado grande."),
  "Comida": meal("Pasta sin gluten a la boloñesa (con carne picada de ternera)",
    [ing("Pasta sin gluten (fusilli maiz-arroz)", 100, "g", C_CEREAL),
     ing("Ternera magra picada", 220, "g", C_CARNE),
     ing("Tomate triturado (bote)", 250, "g", C_LEGUM),
     ing("Cebolla", 60, "g", C_VERD), ing("Ajo", 1, "ud", C_VERD),
     ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Pasta sin gluten (fusilli maiz-arroz)", 25, "g", C_CEREAL), ing("Ternera magra picada", 50, "g", C_CARNE)],
    nota="Pasta (45 g Lydia / 55 g Ruben aprox.). Sofreir la cebolla y el ajo picados, añadir la ternera picada y dorar bien, incorporar el tomate triturado y cocinar 15 min a fuego medio. Mezclar con la pasta recien cocida. Rapida de montar mientras seguis con el resto del cocinado."),
  "Merienda": meal("Fruta y yogur",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA)],
    extra_ruben=[ing("Nueces naturales", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Tortilla de patata sin gluten con ensalada",
    [ing("Patata", 300, "g", C_VERD), ing("Huevo campero (M)", 4, "ud", C_CARNE),
     ing("Cebolla", 60, "g", C_VERD), ing("Lechuga", 60, "g", C_VERD),
     ing("Tomate", 80, "g", C_VERD), ing("Aceite de oliva virgen extra", 15, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 100, "g", C_VERD), ing("Huevo campero (M)", 1, "ud", C_CARNE)],
    nota="Cena tranquila de domingo, todo naturalmente sin gluten."),
}

SEMANA_A["prep_domingo"] = {
  "titulo": "Cocinado grande del domingo (al volver del box)",
  "pasos": [
    paso("1. Horno: boniato y verduras asadas",
      [ing_total(SEMANA_A, "Boniato", C_VERD),
       ing("Pimiento rojo", 300, "g", C_VERD),
       ing("Calabacin", 300, "g", C_VERD),
       ing("Cebolla", 200, "g", C_VERD),
       ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
      "Cortar el boniato en dados y las verduras en trozos. Aliñar con el aceite y sal. Poner el boniato en una bandeja y las verduras en otra (van a la vez pero por separado). Horno 200C, 30-35 min."),
    paso("2. Airfryer: salmon",
      [ing_total(SEMANA_A, "Salmon (lomo fresco)", C_PESCA), ing("Limon", 1, "ud", C_VERD)],
      "Salpimentar el salmon con zumo de limon y eneldo. Airfryer 180C, 10-12 min."),
    paso("3. Vitro: arroz, pasta y huevos",
      [ing_total(SEMANA_A, "Arroz basmati", C_CEREAL),
       ing_total(SEMANA_A, "Pasta sin gluten (fusilli maiz-arroz)", C_CEREAL),
       ing("Huevo campero (M)", 6, "ud", C_CARNE)],
      "Cocer el arroz y la pasta en ollas separadas segun el tiempo del paquete. La pasta se pasa por agua fria nada mas escurrirla, para que no se pegue. Cocer los huevos 10-11 min y enfriarlos en agua para pelarlos bien."),
    paso("4. Plancha: pollo, lomo de cerdo y atun fresco",
      [ing_total(SEMANA_A, "Pechuga de pollo", C_CARNE), ing_total(SEMANA_A, "Lomo de cerdo", C_CARNE),
       ing_total(SEMANA_A, "Atun fresco (lomo)", C_PESCA)],
      "Pollo y lomo de cerdo en tacos o filetes, vuelta y vuelta con sal (cocinar por separado). El atun fresco tambien a la plancha, bien hecho por dentro, sin dejar el centro rosado."),
    paso("5. Thermomix: hummus",
      [ing("Garbanzos cocidos (bote o secos)", 250, "g", C_LEGUM), ing("Tahini", 40, "g", C_FRUTOSEC),
       ing("Limon", 1, "ud", C_VERD), ing("Ajo", 1, "ud", C_VERD), ing("Aceite de oliva virgen extra", 25, "g", C_SALSA)],
      "Triturar todo junto hasta que quede cremoso. Añadir un poco de agua si queda demasiado espeso."),
    paso("6. Thermomix: gazpacho / salmorejo (sin pepino, a Lydia no le gusta)",
      [ing("Tomate", 700, "g", C_VERD), ing("Pimiento rojo", 150, "g", C_VERD), ing("Ajo", 1, "ud", C_VERD),
       ing("Aceite de oliva virgen extra", 40, "g", C_SALSA),
       ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 40, "g", C_CEREAL),
       ing("Vinagre de manzana", 20, "g", C_SALSA)],
      "Triturar todos los ingredientes juntos; el pan sin gluten es lo que le da cuerpo, como en un salmorejo. Colar si se quiere mas fino y meter en la nevera bien frio."),
    paso("7. Lavar y cortar para las ensaladas de la semana",
      [ing("Zanahoria", 150, "g", C_VERD), ing("Apio", 200, "g", C_VERD), ing("Tomate cherry", 200, "g", C_VERD)],
      "Lavar, pelar y cortar. Guardar ya listo en tarteras en la nevera para usar directamente en los tuppers de la semana."),
  ],
}
print("Semana A COMPLETA")

# =========================================================================
# SEMANA B
# =========================================================================
SEMANA_B = {
  "nombre": "Semana B",
  "dias": {}
}

SEMANA_B["dias"]["Lunes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con queso fresco batido, miel y nueces",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 80, "g", C_LACTEO), ing("Miel", 10, "g", C_SALSA),
       ing("Nueces naturales", 10, "g", C_FRUTOSEC)]),
    "Ruben": meal("Tostada con pavo y huevo (post-rodaje suave)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE),
       ing("Pechuga de pavo (fresca, no fiambre)", 40, "g", C_CARNE),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de platano con canela",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Platano", 110, "g", C_FRUTA), ing("Canela", 1, "g", C_SALSA)],
      nota="Batir todo junto."),
    meal("Yogur griego, fruta y semillas de chia",
      [ing("Yogur griego natural", 200, "g", C_LACTEO), ing("Melocoton", 250, "g", C_FRUTA),
       ing("Semillas de chia", 10, "g", C_FRUTOSEC), ing("Nueces naturales", 15, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl tupper de patata, pavo y verduras asadas con salsa de yogur",
    [ing("Patata", 220, "g", C_VERD), ing("Pechuga de pavo (fresca, no fiambre)", 250, "g", C_CARNE),
     ing("Yogur griego natural", 40, "g", C_LACTEO), ing("Limon", 1, "ud", C_VERD)],
    extra_ruben=[ing("Patata", 100, "g", C_VERD), ing("Pechuga de pavo (fresca, no fiambre)", 50, "g", C_CARNE)],
    nota="Patata cocida y pavo en tacos (del domingo) + berenjena/pimiento asados (tambien del domingo) con una salsa rapida de yogur+limon+sal."),
  "Merienda": meal("Tortita de arroz con aguacate y pavo",
    [ing("Tortitas de arroz", 3, "ud", C_CEREAL), ing("Aguacate", 60, "g", C_VERD),
     ing("Pechuga de pavo (fresca, no fiambre)", 40, "g", C_CARNE)],
    extra_ruben=[ing("Tortitas de arroz", 2, "ud", C_CEREAL)]),
  "Cena": meal("Salmon marinado con ensalada verde",
    [ing("Salmon (lomo fresco)", 200, "g", C_PESCA),
     ing("Lechuga", 60, "g", C_VERD), ing("Apio", 80, "g", C_VERD),
     ing("Tomate cherry", 80, "g", C_VERD), ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 100, "g", C_VERD)],
    nota="Salmon marinado del domingo, recalentar suave."),
}

SEMANA_B["dias"]["Martes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con atun y tomate",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Atun al natural (lata)", 60, "g", C_LEGUM), ing("Tomate", 50, "g", C_VERD)]),
    "Ruben": meal("Batido de avena y proteina",
      [ing("Copos de avena sin gluten", 60, "g", C_CEREAL), ing("Leche desnatada", 250, "g", C_LACTEO),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS), ing("Platano", 100, "g", C_FRUTA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa con avena",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fresa", 120, "g", C_FRUTA),
       ing("Copos de avena sin gluten", 20, "g", C_CEREAL)],
      nota="Batir todo junto."),
    meal("Kefir, fruta y anacardos",
      [ing("Kefir natural", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Anacardos naturales", 30, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada de lentejas con verduras y huevo (tupper)",
    [ing("Lentejas cocidas (bote o secas)", 250, "g", C_LEGUM), ing("Pimiento rojo", 80, "g", C_VERD),
     ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Cebolla", 40, "g", C_VERD),
     ing("Aceite de oliva virgen extra", 15, "g", C_SALSA), ing("Vinagre de manzana", 5, "g", C_SALSA)],
    extra_ruben=[ing("Lentejas cocidas (bote o secas)", 100, "g", C_LEGUM)],
    nota="En frio, aguanta perfecto de un dia para otro."),
  "Merienda": meal("Yogur con nueces y miel",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Nueces naturales", 15, "g", C_FRUTOSEC),
     ing("Miel", 10, "g", C_SALSA)],
    extra_ruben=[ing("Nueces naturales", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Revuelto de esparragos con pollo",
    [ing("Esparragos verdes", 200, "g", C_VERD), ing("Huevo campero (M)", 3, "ud", C_CARNE),
     ing("Pechuga de pollo", 60, "g", C_CARNE), ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Huevo campero (M)", 1, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 50, "g", C_CEREAL)],
    nota="Pollo comprado y cocinado fresco ese mismo dia (no es del cocinado del domingo): trocear pequeño y saltear antes de añadir el huevo."),
}
print("Semana B: Lunes y Martes OK")

SEMANA_B["dias"]["Miercoles"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con crema de cacahuete, albaricoque y canela",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Crema de cacahuete 100%", 15, "g", C_FRUTOSEC), ing("Albaricoque", 80, "g", C_FRUTA),
       ing("Canela", 1, "g", C_SALSA)],
      nota=""),
    "Ruben": meal("Tostadas con huevo revuelto y pavo (post-series)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Huevo campero (M)", 3, "ud", C_CARNE), ing("Pechuga de pavo (fresca, no fiambre)", 40, "g", C_CARNE),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de frutos rojos",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fruta de temporada (variada)", 130, "g", C_FRUTA)],
      nota="Batir todo junto."),
    meal("Fruta y yogur",
      [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Nectarina", 250, "g", C_FRUTA),
       ing("Almendras crudas", 20, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl de arroz integral, lomo de cerdo y verduras asadas (tupper)",
    [ing("Arroz integral", 100, "g", C_CEREAL), ing("Lomo de cerdo", 250, "g", C_CARNE),
     ing("Salsa de soja sin gluten (tamari)", 15, "g", C_SALSA)],
    extra_ruben=[ing("Arroz integral", 25, "g", C_CEREAL), ing("Lomo de cerdo", 50, "g", C_CARNE)],
    nota="Arroz integral y lomo de cerdo (del domingo) + berenjena/pimiento asados (tambien del domingo), con un chorrito de tamari."),
  "Merienda": meal("Tostada con queso fresco batido y miel",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
     ing("Queso fresco batido pasteurizado 0%", 60, "g", C_LACTEO), ing("Miel", 10, "g", C_SALSA)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL)]),
  "Cena": meal("Gazpacho de sandia con huevo duro",
    [ing("Huevo campero (M)", 2, "ud", C_CARNE)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 50, "g", C_CEREAL),
                 ing("Pechuga de pavo (fresca, no fiambre)", 60, "g", C_CARNE)],
    nota="400 ml del gazpacho de sandia del domingo, bien frio, con huevo duro picado. Muy refrescante para una noche calurosa."),
}

SEMANA_B["dias"]["Jueves"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con mermelada casera de frutos rojos y queso fresco",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 60, "g", C_LACTEO), ing("Fruta de temporada (variada)", 100, "g", C_FRUTA)],
      nota="Mermelada casera rapida: cocer fruta de temporada troceada con un poco de agua unos 10 min, sin azucar añadido."),
    "Ruben": meal("Tostadas con atun (bici/gimnasio)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Atun al natural (lata)", 80, "g", C_LEGUM), ing("Tomate", 60, "g", C_VERD),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de platano con cacao y avena",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
       ing("Cacao desgrasado en polvo sin azucar", 5, "g", C_OTROS), ing("Copos de avena sin gluten", 15, "g", C_CEREAL)],
      nota="Batir todo junto."),
    meal("Kefir, fruta y nueces",
      [ing("Kefir natural", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Nueces naturales", 30, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl de boniato, atun fresco, edamame y aguacate (tupper)",
    [ing("Boniato", 200, "g", C_VERD), ing("Atun fresco (lomo)", 200, "g", C_PESCA),
     ing("Aguacate", 100, "g", C_VERD), ing("Edamame (vaina o desgranado, congelado)", 100, "g", C_VERD),
     ing("Zanahoria", 60, "g", C_VERD), ing("Salsa de soja sin gluten (tamari)", 15, "g", C_SALSA)],
    extra_ruben=[ing("Boniato", 100, "g", C_VERD), ing("Atun fresco (lomo)", 50, "g", C_PESCA)],
    nota="Boniato asado y atun fresco a la plancha (del domingo), en frio."),
  "Merienda": meal("Yogur con fruta",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
    extra_ruben=[ing("Almendras crudas", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Pavo al horno con patata y verduras",
    [ing("Pechuga de pavo (fresca, no fiambre)", 200, "g", C_CARNE),
     ing("Pimiento verde", 100, "g", C_VERD), ing("Cebolla", 80, "g", C_VERD), ing("Patata", 150, "g", C_VERD),
     ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)],
    nota="Pavo restante del domingo, recalentado al horno con verduras nuevas."),
}
print("Semana B: Miercoles y Jueves OK")

SEMANA_B["dias"]["Viernes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con huevo revuelto y espinacas",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Espinacas frescas", 60, "g", C_VERD)]),
    "Ruben": meal("Tostadas con huevo, pavo y miel (post-tirada larga)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Pechuga de pavo (fresca, no fiambre)", 60, "g", C_CARNE),
       ing("Platano", 100, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de melocoton con miel",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Melocoton", 150, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA)],
      nota="Batir todo junto."),
    meal("Fruta y yogur",
      [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Almendras crudas", 15, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada de lentejas con salmon desmenuzado (tupper, dia de compra)",
    [ing("Salmon (lomo fresco)", 100, "g", C_PESCA),
     ing("Lentejas cocidas (bote o secas)", 250, "g", C_LEGUM), ing("Pimiento rojo", 80, "g", C_VERD),
     ing("Cebolla", 40, "g", C_VERD), ing("Aceite de oliva virgen extra", 15, "g", C_SALSA)],
    extra_ruben=[ing("Lentejas cocidas (bote o secas)", 100, "g", C_LEGUM)],
    nota="Con el salmon marinado que sobra del domingo, desmenuzado."),
  "Merienda": meal("Tostada con platano y miel + frutos secos",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
     ing("Platano", 80, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA), ing("Almendras crudas", 15, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL)]),
  "Cena": meal("Merluza en airfryer con pimientos",
    [ing("Merluza (lomo o rodaja)", 350, "g", C_PESCA), ing("Pimiento rojo", 150, "g", C_VERD),
     ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)]),
}

SEMANA_B["dias"]["Sabado"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con queso fresco y fruta",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 80, "g", C_LACTEO), ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
    "Ruben": meal("Avena con platano y miel (pre-ruta larga)",
      [ing("Copos de avena sin gluten", 90, "g", C_CEREAL), ing("Leche desnatada", 200, "g", C_LACTEO),
       ing("Platano", 100, "g", C_FRUTA), ing("Miel", 15, "g", C_SALSA)],
      nota="Durante la ruta: platano/dátiles cada 45-60 min, hidratacion con sales."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa y platano",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fresa", 100, "g", C_FRUTA), ing("Platano", 60, "g", C_FRUTA)],
      nota="Batir todo junto."),
    meal("Fruta y frutos secos",
      [ing("Fruta de temporada (variada)", 200, "g", C_FRUTA), ing("Anacardos naturales", 15, "g", C_FRUTOSEC),
       ing("Platano", 100, "g", C_FRUTA)],
      nota="Si la ruta se alarga, tomar a media mañana en casa nada mas volver, con el batido de recuperacion de la merienda adelantado si hace falta.")),
  "Comida": meal("Comida libre de la semana",
    [], nota="Segunda comida libre opcional (recordar: maximo 1-2 por semana en total, ajustar con la del domingo si aplica)."),
  "Merienda": almuerzo(
    meal("Batido de platano y fresa",
      [ing("Leche desnatada", 200, "g", C_LACTEO), ing("Platano", 80, "g", C_FRUTA), ing("Fresa", 80, "g", C_FRUTA)],
      nota="A su hora habitual."),
    meal("Batido de recuperacion",
      [ing("Leche desnatada", 250, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 30, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)],
      nota="Nada mas terminar la ruta o al llegar a casa.")),
  "Cena": meal("Hamburguesa casera de ternera sin pan, con boniato frito",
    [ing("Ternera magra picada", 350, "g", C_CARNE), ing("Boniato", 300, "g", C_VERD),
     ing("Lechuga", 60, "g", C_VERD), ing("Tomate", 80, "g", C_VERD), ing("Cebolla", 40, "g", C_VERD)],
    extra_ruben=[ing("Ternera magra picada", 100, "g", C_CARNE), ing("Boniato", 150, "g", C_VERD)],
    nota="Cena de fin de semana: formar las hamburguesas a mano con sal y especias, plancha o airfryer 180C 8-10 min; el boniato en bastones al airfryer 180C 15-18 min como si fueran patatas fritas. Se sirve sin pan, con la ensalada."),
}

SEMANA_B["dias"]["Domingo"] = {
  "Desayuno": meal("Tortitas de avena y platano (pre-Hyrox)",
    [ing("Copos de avena sin gluten", 70, "g", C_CEREAL),
     ing("Platano", 180, "g", C_FRUTA), ing("Huevo campero (M)", 3, "ud", C_CARNE),
     ing("Canela", 1, "g", C_SALSA), ing("Miel", 10, "g", C_SALSA)],
    extra_ruben=[ing("Copos de avena sin gluten", 20, "g", C_CEREAL), ing("Huevo campero (M)", 1, "ud", C_CARNE)],
    nota="Triturar la avena, el platano y los huevos hasta obtener una masa fina; añadir la canela. Tortitas pequeñas en sarten antiadherente, 2-3 min por lado."),
  "Almuerzo": meal("Recuperacion post-Hyrox: huevos revueltos y tostada",
    [ing("Huevo campero (M)", 4, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
     ing("Fruta de temporada (variada)", 200, "g", C_FRUTA), ing("Kefir natural", 200, "g", C_LACTEO)],
    extra_ruben=[ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 40, "g", C_CEREAL)]),
  "Comida": meal("Arroz integral con verduras y pavo",
    [ing("Arroz integral", 100, "g", C_CEREAL), ing("Pechuga de pavo (fresca, no fiambre)", 200, "g", C_CARNE),
     ing("Pimiento verde", 100, "g", C_VERD), ing("Cebolla", 60, "g", C_VERD), ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Arroz integral", 25, "g", C_CEREAL)],
    nota="Arroz (45 g Lydia / 55 g Ruben aprox.). Rapido de montar mientras seguis con el cocinado grande de la semana que empieza."),
  "Merienda": meal("Fruta y yogur",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA)],
    extra_ruben=[ing("Anacardos naturales", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Langostinos a la plancha con ensalada",
    [ing("Langostinos (pelados, crudos)", 300, "g", C_PESCA),
     ing("Aceite de oliva virgen extra", 10, "g", C_SALSA), ing("Lechuga", 60, "g", C_VERD),
     ing("Tomate cherry", 80, "g", C_VERD), ing("Limon", 1, "ud", C_VERD)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)],
    nota="300 g de langostinos pelados a la plancha con ajo y perejil (bien hechos). Cena ligera de domingo."),
}

SEMANA_B["prep_domingo"] = {
  "titulo": "Cocinado grande del domingo (al volver del box)",
  "pasos": [
    paso("1. Horno: patata, boniato y verduras asadas",
      [ing_total(SEMANA_B, "Patata", C_VERD), ing_total(SEMANA_B, "Boniato", C_VERD),
       ing("Berenjena", 300, "g", C_VERD), ing("Pimiento verde", 300, "g", C_VERD), ing("Cebolla", 200, "g", C_VERD),
       ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
      "Cortar la patata y el boniato en dados (bandeja aparte) y la berenjena/pimiento verde/cebolla en trozos (otra bandeja). Aliñar con el aceite y sal. Horno 200C, 30-35 min."),
    paso("2. Airfryer: salmon marinado",
      [ing_total(SEMANA_B, "Salmon (lomo fresco)", C_PESCA), ing("Salsa de soja sin gluten (tamari)", 15, "g", C_SALSA),
       ing("Limon", 1, "ud", C_VERD), ing("Ajo", 1, "ud", C_VERD)],
      "Marinar el salmon 15 min con la soja, el zumo de limon y el ajo picado. Airfryer 180C, 10-12 min."),
    paso("3. Vitro: arroz integral y huevos",
      [ing_total(SEMANA_B, "Arroz integral", C_CEREAL), ing("Huevo campero (M)", 6, "ud", C_CARNE)],
      "Cocer el arroz integral segun el tiempo del paquete. Cocer los huevos 10-11 min y enfriarlos en agua para pelarlos bien."),
    paso("4. Plancha: pavo, lomo de cerdo y atun fresco",
      [ing_total(SEMANA_B, "Pechuga de pavo (fresca, no fiambre)", C_CARNE), ing_total(SEMANA_B, "Lomo de cerdo", C_CARNE),
       ing_total(SEMANA_B, "Atun fresco (lomo)", C_PESCA)],
      "Pavo y lomo de cerdo en tacos o filetes con las especias que mas os gusten (comino, pimenton, oregano), cocinar por separado. Atun fresco a la plancha vuelta y vuelta, bien hecho por dentro, sin dejar el centro rosado."),
    paso("5. Thermomix: gazpacho de sandia (sin pepino, a Lydia no le gusta)",
      [ing("Sandia", 500, "g", C_FRUTA), ing("Tomate", 300, "g", C_VERD), ing("Ajo", 1, "ud", C_VERD),
       ing("Aceite de oliva virgen extra", 30, "g", C_SALSA)],
      "Triturar todo junto con una pizca de sal. Colar si se quiere mas fino y dejar bien frio en la nevera; es una bebida refrescante para las noches de mas calor."),
    paso("6. Thermomix: ajoblanco ligero (opcional, para variar)",
      [ing("Almendras crudas", 60, "g", C_FRUTOSEC), ing("Ajo", 1, "ud", C_VERD),
       ing("Aceite de oliva virgen extra", 20, "g", C_SALSA), ing("Vinagre de manzana", 10, "g", C_SALSA)],
      "Triturar las almendras con el ajo, el aceite, el vinagre y agua hasta que quede cremoso. Se puede usar en vez del gazpacho de sandia si apetece variar."),
    paso("7. Lavar y cortar para las ensaladas de la semana",
      [ing("Apio", 200, "g", C_VERD), ing("Zanahoria", 150, "g", C_VERD), ing("Tomate cherry", 200, "g", C_VERD)],
      "Lavar, pelar y cortar. Guardar ya listo en tarteras en la nevera para usar directamente en los tuppers de la semana."),
  ],
}
print("Semana B COMPLETA")

# =========================================================================
# SEMANA C
# =========================================================================
SEMANA_C = {
  "nombre": "Semana C",
  "dias": {}
}

SEMANA_C["dias"]["Lunes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con crema de cacahuete, albaricoque y canela",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Crema de cacahuete 100%", 15, "g", C_FRUTOSEC), ing("Albaricoque", 80, "g", C_FRUTA), ing("Canela", 1, "g", C_SALSA)]),
    "Ruben": meal("Tostada doble con huevo y platano (post-rodaje suave)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Platano", 100, "g", C_FRUTA), ing("Nueces naturales", 20, "g", C_FRUTOSEC)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de platano con avena y miel",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
       ing("Copos de avena sin gluten", 20, "g", C_CEREAL), ing("Miel", 10, "g", C_SALSA)],
      nota="Batir todo junto."),
    meal("Yogur, fruta y semillas de chia",
      [ing("Yogur natural sin azucar", 250, "g", C_LACTEO), ing("Fruta de temporada (variada)", 250, "g", C_FRUTA),
       ing("Semillas de chia", 10, "g", C_FRUTOSEC), ing("Nueces naturales", 15, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl tupper de patata, pollo especiado, brocoli y coliflor",
    [ing("Patata", 200, "g", C_VERD), ing("Pechuga de pollo", 200, "g", C_CARNE),
     ing("Yogur natural sin azucar", 40, "g", C_LACTEO), ing("Limon", 1, "ud", C_VERD)],
    extra_ruben=[ing("Patata", 100, "g", C_VERD), ing("Pechuga de pollo", 50, "g", C_CARNE)],
    nota="Patata cocida y pollo especiado (del domingo) + brocoli/coliflor asados (tambien del domingo), con una salsa rapida de yogur+limon."),
  "Merienda": meal("Tostada con hummus de remolacha",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL)],
    nota="60 g de hummus de remolacha del domingo por encima."),
  "Cena": meal("Salmon a la plancha con ensalada",
    [ing("Salmon (lomo fresco)", 200, "g", C_PESCA),
     ing("Lechuga", 60, "g", C_VERD), ing("Tomate", 100, "g", C_VERD), ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Boniato", 100, "g", C_VERD)],
    nota="Salmon del domingo, recalentado suave."),
}

SEMANA_C["dias"]["Martes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con queso fresco y tomate",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 80, "g", C_LACTEO), ing("Tomate cherry", 50, "g", C_VERD)]),
    "Ruben": meal("Porridge de avena con melocoton",
      [ing("Copos de avena sin gluten", 80, "g", C_CEREAL), ing("Leche desnatada", 250, "g", C_LACTEO),
       ing("Melocoton", 100, "g", C_FRUTA), ing("Canela", 1, "g", C_SALSA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa con avena",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fresa", 120, "g", C_FRUTA),
       ing("Copos de avena sin gluten", 20, "g", C_CEREAL)],
      nota="Batir todo junto."),
    meal("Kefir, fruta y anacardos",
      [ing("Kefir natural", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Anacardos naturales", 30, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada fria de pasta sin gluten con atun (tupper)",
    [ing("Pasta sin gluten (fusilli maiz-arroz)", 100, "g", C_CEREAL), ing("Atun al natural (lata)", 120, "g", C_LEGUM),
     ing("Tomate cherry", 100, "g", C_VERD), ing("Aceitunas negras sin hueso", 30, "g", C_LEGUM),
     ing("Aceite de oliva virgen extra", 15, "g", C_SALSA)],
    extra_ruben=[ing("Pasta sin gluten (fusilli maiz-arroz)", 25, "g", C_CEREAL), ing("Atun al natural (lata)", 40, "g", C_LEGUM)],
    nota="Pasta (45 g Lydia / 55 g Ruben aprox.), cocida el domingo (se enfrio en agua fria para que no se pegue) + atun + tomate cherry + aceitunas, en frio con AOVE. Ideal para el calor."),
  "Merienda": meal("Yogur con nueces y miel",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Nueces naturales", 15, "g", C_FRUTOSEC), ing("Miel", 10, "g", C_SALSA)],
    extra_ruben=[ing("Nueces naturales", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Revuelto de esparragos con lomo de cerdo",
    [ing("Lomo de cerdo", 100, "g", C_CARNE),
     ing("Esparragos verdes", 200, "g", C_VERD), ing("Huevo campero (M)", 3, "ud", C_CARNE),
     ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Lomo de cerdo", 80, "g", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 50, "g", C_CEREAL)],
    nota="Lomo de cerdo comprado y cocinado fresco ese mismo dia (no es del cocinado del domingo): trocear pequeño y saltear antes de añadir el huevo."),
}
print("Semana C: Lunes y Martes OK")

SEMANA_C["dias"]["Miercoles"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con aguacate y tomate",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Aguacate", 50, "g", C_VERD), ing("Tomate cherry", 40, "g", C_VERD)]),
    "Ruben": meal("Tostadas con huevo revuelto y pollo (post-series)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Huevo campero (M)", 3, "ud", C_CARNE), ing("Pechuga de pollo", 40, "g", C_CARNE),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa con canela",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fresa", 130, "g", C_FRUTA), ing("Canela", 1, "g", C_SALSA)],
      nota="Batir todo junto."),
    meal("Fruta y yogur",
      [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Ciruela", 250, "g", C_FRUTA),
       ing("Almendras crudas", 20, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Bowl de boniato, pavo y brocoli con salsa de tahini (tupper)",
    [ing("Boniato", 200, "g", C_VERD), ing("Pechuga de pavo (fresca, no fiambre)", 150, "g", C_CARNE),
     ing("Tahini", 15, "g", C_FRUTOSEC), ing("Limon", 1, "ud", C_VERD)],
    extra_ruben=[ing("Boniato", 100, "g", C_VERD), ing("Pechuga de pavo (fresca, no fiambre)", 50, "g", C_CARNE)],
    nota="Boniato, pavo y brocoli (del domingo), con salsa de tahini+limon+agua."),
  "Merienda": meal("Tostada con crema de cacahuete",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL), ing("Crema de cacahuete 100%", 20, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL)]),
  "Cena": meal("Gazpacho de sandia con atun",
    [ing("Atun al natural (lata)", 80, "g", C_LEGUM)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 50, "g", C_CEREAL)],
    nota="400 ml de gazpacho de sandia del domingo, bien frio, con atun escurrido por encima."),
}

SEMANA_C["dias"]["Jueves"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con mermelada casera y queso fresco",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 60, "g", C_LACTEO), ing("Fruta de temporada (variada)", 100, "g", C_FRUTA)]),
    "Ruben": meal("Tostadas con atun (bici/gimnasio)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Atun al natural (lata)", 80, "g", C_LEGUM), ing("Tomate", 60, "g", C_VERD),
       ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de frutos rojos con avena",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Fruta de temporada (variada)", 120, "g", C_FRUTA),
       ing("Copos de avena sin gluten", 20, "g", C_CEREAL)],
      nota="Batir todo junto."),
    meal("Kefir, fruta y nueces",
      [ing("Kefir natural", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Nueces naturales", 30, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada de arroz con atun fresco, brocoli y huevo (tupper)",
    [ing("Arroz basmati", 100, "g", C_CEREAL), ing("Atun fresco (lomo)", 150, "g", C_PESCA),
     ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Aceite de oliva virgen extra", 15, "g", C_SALSA)],
    extra_ruben=[ing("Arroz basmati", 25, "g", C_CEREAL), ing("Atun fresco (lomo)", 50, "g", C_PESCA)],
    nota="Arroz (45 g Lydia / 55 g Ruben aprox.) y atun fresco a la plancha (del domingo) + brocoli (tambien del domingo) + huevo cocido, en frio."),
  "Merienda": meal("Yogur con fruta",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)],
    extra_ruben=[ing("Almendras crudas", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Pollo al horno con especias, patata y verduras",
    [ing("Pechuga de pollo", 200, "g", C_CARNE), ing("Patata", 200, "g", C_VERD),
     ing("Pimiento rojo", 100, "g", C_VERD), ing("Especias variadas (oregano, comino, pimenton, etc.)", 3, "g", C_SALSA),
     ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)],
    nota="Cena cocinada fresca, horno 200C 25-30 min."),
}
print("Semana C: Miercoles y Jueves OK")

SEMANA_C["dias"]["Viernes"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con huevo revuelto y espinacas",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Espinacas frescas", 60, "g", C_VERD)]),
    "Ruben": meal("Tostadas con huevo, pollo y miel (post-tirada larga)",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 100, "g", C_CEREAL),
       ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Pechuga de pollo", 60, "g", C_CARNE),
       ing("Platano", 100, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA)]),
  },
  "Almuerzo": almuerzo(
    meal("Batido de melocoton con miel",
      [ing("Leche desnatada", 220, "g", C_LACTEO), ing("Melocoton", 150, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA)],
      nota="Batir todo junto."),
    meal("Fruta y yogur",
      [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA),
       ing("Almendras crudas", 15, "g", C_FRUTOSEC),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 20, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)])),
  "Comida": meal("Ensalada de garbanzos con salmon desmenuzado (tupper, dia de compra)",
    [ing("Salmon (lomo fresco)", 100, "g", C_PESCA),
     ing("Garbanzos cocidos (bote o secos)", 250, "g", C_LEGUM), ing("Apio", 80, "g", C_VERD),
     ing("Tomate", 100, "g", C_VERD), ing("Aceite de oliva virgen extra", 15, "g", C_SALSA)],
    extra_ruben=[ing("Garbanzos cocidos (bote o secos)", 100, "g", C_LEGUM)],
    nota="Con el salmon que sobra del domingo, desmenuzado."),
  "Merienda": meal("Tostada con platano y miel + frutos secos",
    [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL),
     ing("Platano", 80, "g", C_FRUTA), ing("Miel", 10, "g", C_SALSA), ing("Almendras crudas", 15, "g", C_FRUTOSEC)],
    extra_ruben=[ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 30, "g", C_CEREAL)]),
  "Cena": meal("Merluza al papillote con verduras",
    [ing("Merluza (lomo o rodaja)", 350, "g", C_PESCA), ing("Calabacin", 150, "g", C_VERD),
     ing("Tomate cherry", 80, "g", C_VERD), ing("Limon", 1, "ud", C_VERD), ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Patata", 150, "g", C_VERD)],
    nota="Papillote en horno o vitro con tapa, 180C 15-18 min."),
}

SEMANA_C["dias"]["Sabado"] = {
  "Desayuno": {
    "Lydia": meal("Tostada con queso fresco batido y fruta",
      [ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
       ing("Queso fresco batido pasteurizado 0%", 80, "g", C_LACTEO), ing("Fruta de temporada (variada)", 150, "g", C_FRUTA)]),
    "Ruben": meal("Avena con platano y miel (pre-ruta larga)",
      [ing("Copos de avena sin gluten", 90, "g", C_CEREAL), ing("Leche desnatada", 200, "g", C_LACTEO),
       ing("Platano", 100, "g", C_FRUTA), ing("Miel", 15, "g", C_SALSA)],
      nota="Durante la ruta: fruta desecada/platano cada 45-60 min, hidratacion con sales."),
  },
  "Almuerzo": almuerzo(
    meal("Batido de fresa con platano y yogur",
      [ing("Leche desnatada", 180, "g", C_LACTEO), ing("Yogur natural sin azucar", 80, "g", C_LACTEO),
       ing("Fresa", 100, "g", C_FRUTA), ing("Platano", 60, "g", C_FRUTA)],
      nota="Batir todo junto."),
    meal("Fruta y frutos secos",
      [ing("Fruta de temporada (variada)", 200, "g", C_FRUTA), ing("Almendras crudas", 15, "g", C_FRUTOSEC),
       ing("Platano", 100, "g", C_FRUTA)],
      nota="Si la ruta se alarga, tomar a media mañana en casa nada mas volver, con el batido de recuperacion de la merienda adelantado si hace falta.")),
  "Comida": meal("Comida libre de la semana",
    [], nota="Aprovechar el sabado para la comida libre (recordar: maximo 1-2 comidas libres por semana en total)."),
  "Merienda": almuerzo(
    meal("Batido de platano y fresa",
      [ing("Leche desnatada", 200, "g", C_LACTEO), ing("Platano", 80, "g", C_FRUTA), ing("Fresa", 80, "g", C_FRUTA)],
      nota="A su hora habitual."),
    meal("Batido de recuperacion",
      [ing("Leche desnatada", 250, "g", C_LACTEO), ing("Platano", 100, "g", C_FRUTA),
       ing("Proteina en polvo (whey o vegetal, sin gluten)", 30, "g", C_OTROS),
       ing("Creatina monohidrato", 5, "g", C_OTROS)],
      nota="Nada mas terminar la ruta o al llegar a casa.")),
  "Cena": meal("Albondigas de ternera con tomate y arroz",
    [ing("Ternera magra picada", 350, "g", C_CARNE), ing("Tomate triturado (bote)", 200, "g", C_LEGUM),
     ing("Arroz basmati", 100, "g", C_CEREAL), ing("Ajo", 1, "ud", C_VERD), ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Ternera magra picada", 100, "g", C_CARNE), ing("Arroz basmati", 40, "g", C_CEREAL)],
    nota="Formar albondigas con la ternera+ajo+sal, dorar y terminar de cocinar en la salsa de tomate 15 min. Cena de fin de semana."),
}

SEMANA_C["dias"]["Domingo"] = {
  "Desayuno": meal("Tortitas de avena y platano (pre-Hyrox)",
    [ing("Copos de avena sin gluten", 70, "g", C_CEREAL),
     ing("Platano", 180, "g", C_FRUTA), ing("Huevo campero (M)", 3, "ud", C_CARNE),
     ing("Canela", 1, "g", C_SALSA), ing("Miel", 10, "g", C_SALSA)],
    extra_ruben=[ing("Copos de avena sin gluten", 20, "g", C_CEREAL), ing("Huevo campero (M)", 1, "ud", C_CARNE)],
    nota="Triturar la avena, el platano y los huevos hasta obtener una masa fina; añadir la canela. Tortitas pequeñas en sarten antiadherente, 2-3 min por lado."),
  "Almuerzo": meal("Recuperacion post-Hyrox: huevos revueltos y tostada",
    [ing("Huevo campero (M)", 4, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 60, "g", C_CEREAL),
     ing("Fruta de temporada (variada)", 200, "g", C_FRUTA), ing("Kefir natural", 200, "g", C_LACTEO)],
    extra_ruben=[ing("Huevo campero (M)", 2, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 40, "g", C_CEREAL)]),
  "Comida": meal("Pasta sin gluten con tomate, garbanzos y verduras",
    [ing("Pasta sin gluten (fusilli maiz-arroz)", 90, "g", C_CEREAL), ing("Tomate triturado (bote)", 200, "g", C_LEGUM),
     ing("Garbanzos cocidos (bote o secos)", 150, "g", C_LEGUM), ing("Calabacin", 100, "g", C_VERD),
     ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
    extra_ruben=[ing("Pasta sin gluten (fusilli maiz-arroz)", 25, "g", C_CEREAL)],
    nota="Pasta (40 g Lydia / 50 g Ruben aprox., ya lleva garbanzos de mas hidrato). Rapido de montar mientras seguis con el cocinado grande de la semana que empieza."),
  "Merienda": meal("Fruta y yogur",
    [ing("Yogur natural sin azucar", 200, "g", C_LACTEO), ing("Fruta de temporada (variada)", 200, "g", C_FRUTA)],
    extra_ruben=[ing("Almendras crudas", 15, "g", C_FRUTOSEC)]),
  "Cena": meal("Revuelto de gambas con verduras",
    [ing("Langostinos (pelados, crudos)", 250, "g", C_PESCA), ing("Huevo campero (M)", 3, "ud", C_CARNE),
     ing("Espinacas frescas", 100, "g", C_VERD), ing("Ajo", 1, "ud", C_VERD), ing("Aceite de oliva virgen extra", 8, "g", C_SALSA)],
    extra_ruben=[ing("Huevo campero (M)", 1, "ud", C_CARNE), ing("Pan de trigo sarraceno sin gluten (o multicereales sin gluten)", 50, "g", C_CEREAL)],
    nota="Gambas bien hechas (nunca poco hechas). Cena tranquila de domingo."),
}

SEMANA_C["prep_domingo"] = {
  "titulo": "Cocinado grande del domingo (al volver del box)",
  "pasos": [
    paso("1. Horno: patata, boniato, brocoli y coliflor asados",
      [ing_total(SEMANA_C, "Patata", C_VERD), ing_total(SEMANA_C, "Boniato", C_VERD),
       ing("Brocoli", 300, "g", C_VERD), ing("Coliflor", 300, "g", C_VERD),
       ing("Especias variadas (oregano, comino, pimenton, etc.)", 5, "g", C_SALSA),
       ing("Aceite de oliva virgen extra", 10, "g", C_SALSA)],
      "Cortar la patata y el boniato en dados (bandeja aparte) y el brocoli/coliflor en arbolitos (otra bandeja). Aliñar con el aceite, sal y las especias. Horno 200C, 25-30 min."),
    paso("2. Airfryer: salmon",
      [ing_total(SEMANA_C, "Salmon (lomo fresco)", C_PESCA)],
      "Salpimentar el salmon. Airfryer 180C, 10-12 min."),
    paso("3. Vitro: arroz basmati, pasta sin gluten y huevos",
      [ing_total(SEMANA_C, "Arroz basmati", C_CEREAL),
       ing_total(SEMANA_C, "Pasta sin gluten (fusilli maiz-arroz)", C_CEREAL),
       ing("Huevo campero (M)", 6, "ud", C_CARNE)],
      "Cocer el arroz y la pasta en ollas separadas segun el tiempo del paquete (la pasta se pasa por agua fria nada mas escurrirla, para que no se pegue). Cocer los huevos 10-11 min y enfriarlos en agua para pelarlos bien."),
    paso("4. Plancha: pollo especiado, pavo y atun fresco",
      [ing_total(SEMANA_C, "Pechuga de pollo", C_CARNE), ing_total(SEMANA_C, "Pechuga de pavo (fresca, no fiambre)", C_CARNE),
       ing_total(SEMANA_C, "Atun fresco (lomo)", C_PESCA),
       ing("Especias variadas (oregano, comino, pimenton, etc.)", 5, "g", C_SALSA)],
      "Pollo en tacos con las especias y pavo en filetes, vuelta y vuelta (cocinar por separado). Atun fresco tambien a la plancha vuelta y vuelta, bien hecho por dentro, sin dejar el centro rosado."),
    paso("5. Thermomix: hummus de remolacha",
      [ing("Garbanzos cocidos (bote o secos)", 200, "g", C_LEGUM), ing("Remolacha cocida al natural", 150, "g", C_VERD),
       ing("Tahini", 30, "g", C_FRUTOSEC), ing("Limon", 1, "ud", C_VERD), ing("Ajo", 1, "ud", C_VERD),
       ing("Aceite de oliva virgen extra", 25, "g", C_SALSA)],
      "Triturar todo junto hasta que quede cremoso. Queda de un color rosa muy vistoso, perfecto para untar en tostadas."),
    paso("6. Thermomix: gazpacho de sandia (sin pepino, a Lydia no le gusta)",
      [ing("Sandia", 500, "g", C_FRUTA), ing("Tomate", 400, "g", C_VERD), ing("Ajo", 1, "ud", C_VERD),
       ing("Aceite de oliva virgen extra", 30, "g", C_SALSA)],
      "Triturar todo junto con una pizca de sal. Colar si se quiere mas fino y dejar bien frio en la nevera."),
    paso("7. Lavar y cortar para las ensaladas de la semana",
      [ing("Apio", 200, "g", C_VERD), ing("Tomate cherry", 150, "g", C_VERD)],
      "Lavar, pelar y cortar. Guardar ya listo en tarteras en la nevera para usar directamente en los tuppers de la semana. Nota: la ternera de las albondigas del sabado se compra y se cocina fresca ese mismo dia, no hace falta prepararla hoy."),
  ],
}
print("Semana C COMPLETA")

# =========================================================================
# EXPORTAR JSON
# =========================================================================
DATA = {"A": SEMANA_A, "B": SEMANA_B, "C": SEMANA_C}
with open("menu_data.json", "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
print("menu_data.json escrito. Total categorias distintas:", len(set(CATS.values())))
print(sorted(set(CATS.values())))
