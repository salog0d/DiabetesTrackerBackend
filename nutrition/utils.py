clasificacion_nutricional = {
    'fibras': [
        "beet_salad", "bruschetta", "caesar_salad", "caprese_salad", "edamame",
        "falafel", "french_onion_soup", "greek_salad", "guacamole", "hummus",
        "miso_soup", "seaweed_salad", "spring_rolls", "samosa"
    ],
    'carbohidratos': [
        "apple_pie", "baklava", "beignets", "bread_pudding", "breakfast_burrito",
        "cannoli", "carrot_cake", "cheesecake", "chocolate_cake", "chocolate_mousse",
        "churros", "club_sandwich", "creme_brulee", "croque_madame", "cup_cakes",
        "donuts", "dumplings", "french_fries", "french_toast", "fried_rice",
        "frozen_yogurt", "garlic_bread", "gnocchi", "grilled_cheese_sandwich",
        "ice_cream", "lasagna", "lobster_roll_sandwich", "macaroni_and_cheese",
        "macarons", "nachos", "onion_rings", "pad_thai", "pancakes", "panna_cotta",
        "pizza", "poutine", "ramen", "ravioli", "red_velvet_cake", "risotto",
        "spaghetti_bolognese", "spaghetti_carbonara", "strawberry_shortcake",
        "tacos", "takoyaki", "tiramisu", "waffles"
    ],
    'grasas': [
        "baby_back_ribs", "baklava", "beignets", "bread_pudding", "cheese_plate",
        "cheesecake", "chicken_wings", "churros", "creme_brulee", "deviled_eggs",
        "donuts", "foie_gras", "fried_calamari", "fried_rice",
        "grilled_cheese_sandwich", "hamburger", "ice_cream", "macaroni_and_cheese",
        "nachos", "onion_rings", "poutine", "spring_rolls", "tiramisu"
    ],
    'proteinas': [
        "baby_back_ribs", "beef_carpaccio", "beef_tartare", "bibimbap", "ceviche",
        "cheese_plate", "chicken_curry", "chicken_quesadilla", "chicken_wings",
        "clam_chowder", "crab_cakes", "deviled_eggs", "edamame", "eggs_benedict",
        "escargots", "filet_mignon", "fish_and_chips", "foie_gras", "grilled_salmon",
        "hamburger", "hot_dog", "huevos_rancheros", "hummus", "lobster_bisque",
        "lobster_roll_sandwich", "mussels", "omelette", "oysters", "paella",
        "peking_duck", "pho", "pork_chop", "prime_rib", "pulled_pork_sandwich",
        "ramen", "sashimi", "scallops", "shrimp_and_grits", "steak", "sushi",
        "tacos", "takoyaki", "tuna_tartare"
    ]
}


class NutricionUtils:

    @staticmethod
    def buscar_alimento_por_categoria(alimento):
        return [
            categoria for categoria, lista in clasificacion_nutricional.items()
            if alimento in lista
        ]

    @staticmethod
    def encontrar_alimentos_multiples():
        alimentos = set(
            item for lista in clasificacion_nutricional.values() for item in lista
        )
        resultado = {}
        for alimento in alimentos:
            categorias = NutricionUtils.buscar_alimento_por_categoria(alimento)
            if len(categorias) > 1:
                resultado[alimento] = categorias
        return resultado

    @staticmethod
    def obtener_estadisticas():
        alimentos_unicos = set(
            item for lista in clasificacion_nutricional.values() for item in lista
        )
        multiples = NutricionUtils.encontrar_alimentos_multiples()

        return {
            'total_por_categoria': {
                categoria: len(lista)
                for categoria, lista in clasificacion_nutricional.items()
            },
            'alimentos_unicos': len(alimentos_unicos),
            'alimentos_multiples': len(multiples),
            'total_entradas': sum(len(lista) for lista in clasificacion_nutricional.values())
        }

    @staticmethod
    def filtrar_por_categoria(*categorias_deseadas):
        alimentos = set(
            item for lista in clasificacion_nutricional.values() for item in lista
        )
        filtrados = []
        for alimento in alimentos:
            categorias = set(NutricionUtils.buscar_alimento_por_categoria(alimento))
            if categorias == set(categorias_deseadas):
                filtrados.append(alimento)
        return filtrados
