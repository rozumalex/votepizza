from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

from ..models import Pizza, Topping
from ..serializers import PizzaSerializer


client = Client()


class PizzaListViewTest(TestCase):
    def setUp(self):
        Pizza.objects.create(name='Pepperoni', price='3.99')
        Pizza.objects.create(name='Margherita', price='4.50')
        Pizza.objects.create(name='Four Seas', price='5')
        Pizza.objects.create(name='Hawaiian', price='12')

    def test_get_all_pizza(self):
        response = client.get(reverse('pizza:pizza-list'))
        pizza = Pizza.objects.all()
        serializer = PizzaSerializer(pizza, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PizzaDetailViewTest(TestCase):
    def setUp(self):
        self.pepperoni = Pizza.objects.create(name='Pepperoni', price='3.99')
        self.margherita = Pizza.objects.create(name='Margherita', price='4.50')
        self.four_seasons = Pizza.objects.create(name='Four Seas', price='5')
        self.hawaiian = Pizza.objects.create(name='Hawaiian', price='12')

    def test_get_valid_single_pizza(self):
        response = client.get(
            reverse('pizza:pizza-detail', kwargs={'pk': self.pepperoni.pk}))
        pepperoni = Pizza.objects.get(pk=self.pepperoni.pk)
        serializer = PizzaSerializer(pepperoni)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_pizza(self):
        response = client.get(
            reverse('pizza:pizza-detail', kwargs={'pk': 217}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPizzaTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'Margherita',
            'price': 3.99,
        }
        self.invalid_name_data = {
            'name': '',
            'price': 3.99
        }
        self.invalid_price_data = {
            'name': 'Pepperoni',
            'price': -3.99
        }

    def test_create_valid_pizza(self):
        response = client.post(
            reverse('pizza:pizza-list'),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_name_pizza(self):
        response = client.post(
            reverse('pizza:pizza-list'),
            data=json.dumps(self.invalid_name_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_price_pizza(self):
        response = client.post(
            reverse('pizza:pizza-list'),
            data=json.dumps(self.invalid_price_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePizzaTest(TestCase):
    def setUp(self):
        self.hawaiian = Pizza.objects.create(name='Hawaiian', price='4.99')

        self.valid_name_data = {
            'name': 'Hawaii'
        }
        self.invalid_name_data = {
            'name': ''
        }
        self.valid_price_data = {
            'price': 10
        }
        self.invalid_price_data = {
            'price': ''
        }

    def test_valid_name_update_pizza(self):
        response = client.patch(
            reverse('pizza:pizza-detail', kwargs={'pk': self.hawaiian.pk}),
            data=json.dumps(self.valid_name_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_name_update_pizza(self):
        response = client.patch(
            reverse('pizza:pizza-detail', kwargs={'pk': self.hawaiian.pk}),
            data=json.dumps(self.invalid_name_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_price_update_pizza(self):
        response = client.patch(
            reverse('pizza:pizza-detail', kwargs={'pk': self.hawaiian.pk}),
            data=json.dumps(self.valid_price_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_price_update_pizza(self):
        response = client.patch(
            reverse('pizza:pizza-detail', kwargs={'pk': self.hawaiian.pk}),
            data=json.dumps(self.invalid_price_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePizzaTest(TestCase):
    def setUp(self):
        self.pepperoni = Pizza.objects.create(
            name='Pepperoni', price='7.99')

    def test_valid_delete_pizza(self):
        response = client.delete(
            reverse('pizza:pizza-detail', kwargs={'pk': self.pepperoni.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_pizza(self):
        response = client.delete(
            reverse('pizza:pizza-detail', kwargs={'pk': 46}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VoteForPizzaTest(TestCase):
    def setUp(self):
        self.hawaiian = Pizza.objects.create(name='Hawaiian', price='4.99')

    def test_valid_patch_vote_for_pizza(self):
        response = client.patch(
            reverse('pizza:pizza-vote', kwargs={'pk': self.hawaiian.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_post_vote_for_pizza(self):
        response = client.post(
            reverse('pizza:pizza-vote', kwargs={'pk': self.hawaiian.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invalid_get_vote_for_pizza(self):
        response = client.get(
            reverse('pizza:pizza-vote', kwargs={'pk': self.hawaiian.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateNewToppingTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'sausages'
        }
        self.invalid_name_data = {
            'name': ''
        }

    def test_create_valid_topping(self):
        response = client.post(
            reverse('pizza:toppings-list'),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_name_topping(self):
        response = client.post(
            reverse('pizza:toppings-list'),
            data=json.dumps(self.invalid_name_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleToppingTest(TestCase):
    def setUp(self):
        self.sausage = Topping.objects.create(name='sausage')

    def test_valid_delete_topping(self):
        response = client.delete(
            reverse('pizza:toppings-detail', kwargs={'pk': self.sausage.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_topping(self):
        response = client.delete(
            reverse('pizza:toppings-detail', kwargs={'pk': 46}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddToppingToPizzaTest(TestCase):
    def setUp(self):
        self.neapolitana = Pizza.objects.create(name='Neapolitana',
                                                price=12)
        self.valid_data = {
            'name': 'sausages'
        }
        self.invalid_data = {
            'age': 15
        }

    def test_valid_adding_topping_to_pizza(self):
        response = client.post(
            reverse('pizza:pizza-detail', kwargs={'pk': self.neapolitana.pk}),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_adding_topping_to_pizza(self):
        response = client.post(
            reverse('pizza:pizza-detail', kwargs={'pk': self.neapolitana.pk}),
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RemoveToppingFromPizzaTest(TestCase):
    def setUp(self):
        self.neapolitana = Pizza.objects.create(name='Neapolitana',
                                                price=12)
        self.meat = Topping.objects.create(name='meat')
        self.rukkola = Topping.objects.create(name='rukkola')
        self.neapolitana.toppings.add(self.meat, self.rukkola)

    def test_valid_removing_topping_from_pizza(self):
        response = client.delete(
            reverse('pizza:toppings-in-pizza',
                    kwargs={'pk': self.neapolitana.id,
                            'topping_pk': self.rukkola.id}),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_valid_removing_topping_from_pizza_2(self):
        client.delete(
            reverse('pizza:toppings-in-pizza',
                    kwargs={'pk': self.neapolitana.id,
                            'topping_pk': self.rukkola.id}),
            content_type='application/json')
        self.assertFalse(self.rukkola in self.neapolitana.toppings.all())

    def test_valid_removing_topping_from_pizza_3(self):
        client.delete(
            reverse('pizza:toppings-in-pizza',
                    kwargs={'pk': self.neapolitana.id,
                            'topping_pk': self.rukkola.id}),
            content_type='application/json')
        self.assertTrue(self.rukkola in Topping.objects.all())
