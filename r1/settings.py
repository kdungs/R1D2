from .types import (DishType, Restaurant)


BASE = 'http://extranet.novae-restauration.ch/'
URL1 = BASE + 'index.php?frame=1&x={x}&y={y}&z={z}'
URL2 = BASE + '/novae/traiteur/restauration/{html}.html?frame=1'
PARAMS = {
    Restaurant.r1: {
        'x': 'd894ddae3c17b40b4fe7e16519f950f0',
        'y': 'c7b3f79848b99a8e562a1df1d6285365',
        'z': '33',
        'html': 'restaurant-cern',
        'pages': 3,
        'page_structure': (3, 2, 2),
        'dishes': (DishType.menu1, DishType.menu2, DishType.vegetarian,
                   DishType.speciality, DishType.grill, DishType.pasta,
                   DishType.pizza),
        'currency': 'CHF'
    },
    Restaurant.r2: {
        'x': 'ad3f8f75fe1e353b972afcce8e375d6e',
        'y': '81dc9bdb52d04dc20036dbd8313ed055',
        'z': '135',
        'html': 'bon-app',
        'pages': 2,
        'page_structure': (3, 3),
        'dishes': (DishType.menu1, DishType.menu2, DishType.vegetarian,
                   DishType.grill, DishType.pizza, DishType.speciality),
        'currency': 'CHF'
    },
    Restaurant.r3: {
        'x': 'fd7538322d53ecf7f708990e221d5f36',
        'y': 'fd7538322d53ecf7f708990e221d5f36',
        'z': '145',
        'html': 'restaurant-cern-1',
        'pages': 2,
        'page_structure': (3, 3),
        'dishes': (DishType.menu1, DishType.menu2, DishType.menu3,
                   DishType.speciality, DishType.pizza, DishType.grill),
        'currency': 'EUR'
    }
}
