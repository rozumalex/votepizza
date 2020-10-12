from django.test import TestCase

from ..models import Topping, Pizza


class PizzaModelTest(TestCase):
    def setUp(self):
        Pizza.objects.create(name='Pepperoni', price='3.99')
        Topping.objects.create(name='Sausage')

    def test_adding_toppings(self):
        pizza_pepperoni = Pizza.objects.get(name='Pepperoni')
        topping_sausage = Topping.objects.get(name='Sausage')
        pizza_pepperoni.toppings.add(topping_sausage)

        self.assertEqual(pizza_pepperoni.count_toppings(), 1)

    def test_get_pizza(self):
        pizza_pepperoni = Pizza.objects.get(name='Pepperoni')
        self.assertEqual(pizza_pepperoni.name, 'Pepperoni')
