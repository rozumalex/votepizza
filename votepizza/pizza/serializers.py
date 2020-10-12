from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Pizza, Topping


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ('id', 'name',)


class PizzaSerializer(serializers.ModelSerializer):
    toppings = ToppingSerializer(many=True)
    votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Pizza
        fields = ('id', 'name', 'price', 'count_toppings', 'toppings',
                  'votes',)

    def create(self, validated_data):
        toppings_data = validated_data.pop('toppings')
        pizza = Pizza.objects.create(**validated_data)
        for topping_data in toppings_data:
            topping = Topping.objects.filter(name=topping_data['name']).first()
            if not topping:
                topping = Topping.objects.create(name=topping_data['name'])
            pizza.toppings.add(topping)
        return pizza

    def update(self, instance, validated_data):
        try:
            toppings_data = validated_data.pop('toppings')
        except Exception:
            toppings_data = []

        for topping in instance.toppings.all():
            instance.toppings.remove(topping)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.votes = validated_data.get('votes', instance.votes)

        for topping_data in toppings_data:
            try:
                topping = Topping.objects.filter(
                    name=topping_data['name']).first()
            except Exception:
                raise ValidationError
            if not topping:
                topping = Topping.objects.create(name=topping_data['name'])
            instance.toppings.add(topping)
        instance.save()
        return instance
