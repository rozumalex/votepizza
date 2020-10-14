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
    name = serializers.CharField(read_only=True)
    id = serializers.ModelField(model_field=Topping._meta.get_field('id'),
                                required=False)

    class Meta:
        model = Topping
        fields = ('id', 'name',)


class PizzaSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="pizza:pizza-detail", read_only=True)
    vote_url = serializers.HyperlinkedIdentityField(
        view_name="pizza:pizza-vote", read_only=True)
    votes = serializers.IntegerField(read_only=True)
    toppings = ToppingsNoUrlSerializer(many=True, required=True)
    extra_kwargs = {
        'toppings': {'validators': []}
    }

    class Meta:
        model = Pizza
        fields = ('url', 'id', 'name', 'price', 'count_toppings', 'toppings',
                  'vote_url', 'votes',)

    def validate_toppings(self, toppings=None):
        for counter, topping in enumerate(toppings):
            if not isinstance(topping, dict):
                raise ValidationError("Invalid topping data type. Need dict.")

            if not topping.get('id', None):
                raise ValidationError("Topping should have id")
            if not Topping.objects.filter(id=topping['id']).exists():
                raise ValidationError("No such topping")
            if len(topping.keys()) > 1:
                toppings[counter] = dict(id=topping.get('id'))
        return toppings

    @transaction.atomic
    def create(self, validated_data):
        toppings_data = validated_data.pop('toppings')
        pizza = Pizza.objects.create(**validated_data)
        for topping_data in toppings_data:
            topping = Topping.objects.get(id=topping_data['id'])
            pizza.toppings.add(topping)
        return pizza

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'toppings' in validated_data:
            toppings_data = validated_data.pop('toppings')
            for topping in instance.toppings.all():
                instance.toppings.remove(topping)
            for topping_data in toppings_data:
                topping = Topping.objects.get(id=topping_data['id'])
                instance.toppings.add(topping)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.votes = validated_data.get('votes', instance.votes)
        return instance


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = ()
