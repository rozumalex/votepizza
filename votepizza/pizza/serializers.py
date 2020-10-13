from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .models import Pizza, Topping


class ToppingsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="pizza:toppings-detail", read_only=True)

    class Meta:
        model = Topping
        fields = ('url', 'id', 'name',)


class ToppingsNoUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ('name',)
        extra_kwargs = {
            'name': {'validators': []},
        }


class PizzaSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="pizza:pizza-detail", read_only=True)
    vote_url = serializers.HyperlinkedIdentityField(
        view_name="pizza:pizza-vote", read_only=True)
    votes = serializers.IntegerField(read_only=True)
    toppings = ToppingsNoUrlSerializer(many=True, required=False)

    class Meta:
        model = Pizza
        fields = ('url', 'id', 'name', 'price', 'count_toppings', 'toppings',
                  'vote_url', 'votes',)

    @transaction.atomic
    def create(self, validated_data):
        try:
            toppings_data = validated_data.pop('toppings')
        except Exception:
            toppings_data = []
        pizza = Pizza.objects.create(**validated_data)
        for topping_data in toppings_data:
            topping = Topping.objects.filter(name=topping_data['name']).first()
            if not topping:
                topping = Topping.objects.create(name=topping_data['name'])
            pizza.toppings.add(topping)
        return pizza

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'toppings' in validated_data:
            toppings_data = validated_data.pop('toppings')
            for topping in instance.toppings.all():
                instance.toppings.remove(topping)
            for topping_data in toppings_data:
                try:
                    topping = Topping.objects.filter(
                        name=topping_data['name']).first()
                except Exception:
                    topping = False
                if not topping:
                    try:
                        topping = Topping.objects.create(
                            name=topping_data['name'])
                    except Exception:
                        raise ValidationError
                instance.toppings.add(topping)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.votes = validated_data.get('votes', instance.votes)
        instance.save()
        return instance
