from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


from .models import Pizza, Topping
from .serializers import PizzaSerializer, ToppingSerializer


class PizzaListView(APIView):
    def get(self, request, format=None):
        pizza = Pizza.objects.all()
        serializer_context = {
            'request': request
        }
        serializer = PizzaSerializer(pizza,
                                     context=serializer_context,
                                     many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PizzaDetailView(APIView):
    def get(self, request, pk, format=None):
        pizza = get_object_or_404(Pizza, pk=pk)
        serializer_context = {
            'request': request
        }
        serializer = PizzaSerializer(pizza, context=serializer_context)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        pizza = get_object_or_404(Pizza, pk=pk)
        serializer = PizzaSerializer(pizza, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer_context = {
            'request': request
        }
        serializer = ToppingSerializer(data=request.data,
                                       context=serializer_context)
        try:
            topping = Topping.objects.filter(name=request.data['name']).first()
        except Exception:
            raise ValidationError(status.HTTP_400_BAD_REQUEST)
        pizza = get_object_or_404(Pizza, pk=pk)
        if topping in pizza.toppings.all():
            serializer.is_valid()
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not topping:
            if serializer.is_valid():
                serializer.save()
                pizza.toppings.add(serializer.data['id'])
                pizza.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        else:
            pizza.toppings.add(topping.id)
            pizza.save()
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VoteDetailView(APIView):
    def patch(self, request, pk, format=None):
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.votes += 1
        pizza.save()
        return Response({'voted': True})


class ToppingsInPizzaDetailView(APIView):
    def get(self, request, pk, topping_pk, format=None):
        pizza = get_object_or_404(Pizza, pk=pk)
        topping = get_object_or_404(Topping, pk=topping_pk)
        if topping in pizza.toppings.all():
            serializer_context = {
                'request': request
            }
            serializer = ToppingSerializer(topping,
                                           context=serializer_context)
            return Response(serializer.data)
        else:
            raise Http404

    def delete(self, request, pk, topping_pk, format=None):
        topping = get_object_or_404(Topping, pk=topping_pk)
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.toppings.remove(topping)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToppingsListView(APIView):
    def get(self, request, format=None):
        toppings = Topping.objects.all()
        serializer_context = {
            'request': request
        }
        serializer = ToppingSerializer(toppings,
                                       context=serializer_context,
                                       many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ToppingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToppingsDetailView(APIView):
    def get(self, request, pk, format=None):
        topping = get_object_or_404(Topping, pk=pk)
        serializer_context = {
            'request': request
        }
        serializer = ToppingSerializer(topping, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        topping = get_object_or_404(Topping, pk=pk)
        serializer = ToppingSerializer(topping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        topping = get_object_or_404(Topping, pk=pk)
        topping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
