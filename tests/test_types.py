import unittest

from r1 import types
from datetime import date


class TestRestaurant(unittest.TestCase):
    def test_valid_string(self):
        self.assertTrue(types.valid_string_for_restaurant('r1'))
        self.assertTrue(types.valid_string_for_restaurant('r2'))
		self.assertTrue(types.valid_string_for_restaurant('r3'))
        self.assertFalse(types.valid_string_for_restaurant(None))
        self.assertFalse(types.valid_string_for_restaurant(''))
        self.assertFalse(types.valid_string_for_restaurant('r4'))
        self.assertFalse(types.valid_string_for_restaurant('r1r1r1r1'))

    def test_from_string(self):
        self.assertEqual(types.Restaurant.r1,
                         types.restaurant_from_string('r1'))
        self.assertEqual(types.Restaurant.r2,
                         types.restaurant_from_string('r2'))
		self.assertEqual(types.Restaurant.r3,
                         types.restaurant_from_string('r3'))
        self.assertRaises(KeyError, types.restaurant_from_string, None)
        self.assertRaises(KeyError, types.restaurant_from_string, '')
        self.assertRaises(KeyError, types.restaurant_from_string, 'r4')


class TestDishType(unittest.TestCase):
    def test_valid_string(self):
        valid_strs = ['menu1', 'menu2', 'menu3', 'vegetarian', 'speciality', 'grill',
                      'pasta', 'pizza']
        for valid_str in valid_strs:
            self.assertTrue(types.valid_string_for_dishtype(valid_str))
        self.assertFalse(types.valid_string_for_dishtype(None))
        self.assertFalse(types.valid_string_for_dishtype(''))
        self.assertFalse(types.valid_string_for_dishtype('cake'))
        self.assertFalse(types.valid_string_for_dishtype('menu1000'))

    def test_from_string(self):
        expected = {'menu1': types.DishType.menu1,
                    'menu2': types.DishType.menu2,
					'menu3': types.DishType.menu3,
                    'vegetarian': types.DishType.vegetarian,
                    'speciality': types.DishType.speciality,
                    'grill': types.DishType.grill,
                    'pasta': types.DishType.pasta,
                    'pizza': types.DishType.pizza}
        for k, v in expected.items():
            self.assertEqual(v, types.dishtype_from_string(k))
        self.assertRaises(KeyError, types.dishtype_from_string, None)
        self.assertRaises(KeyError, types.dishtype_from_string, '')
        self.assertRaises(KeyError, types.dishtype_from_string, 'cake')


class TestMenuItem(unittest.TestCase):
    def test_creation(self):
        mi = types.MenuItem(types.Restaurant.r1, date.today(),
                            types.DishType.menu1, 'Shit with sauce', 13.37, 'USD')
        self.assertEqual(types.Restaurant.r1, mi.restaurant)
        self.assertEqual(date.today(), mi.date)
        self.assertEqual(types.DishType.menu1, mi.type)
        self.assertEqual('Shit with sauce', mi.name)
        self.assertEqual(13.37, mi.price)
		self.assertEqual('USD', mi.currency)
