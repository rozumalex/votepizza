from rest_framework import serializers

from .models import Pizza, Topping


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ('id', 'name',)


class PizzaSerializer(serializers.HyperlinkedModelSerializer):
    votes = serializers.IntegerField(read_only=True)
    toppings = ToppingSerializer(many=True, required=False)

    class Meta:
        model = Pizza
        fields = ('id', 'name', 'price', 'count_toppings', 'toppings',
                  'votes',)
