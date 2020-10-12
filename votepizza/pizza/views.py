from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Pizza, Topping
from .serializers import PizzaSerializer, ToppingsSerializer


class API(APIView):
    def get(self, request):
        return Response({
            'pizza': reverse("pizza:pizza-list", request=request),
            'toppings': reverse("pizza:toppings-list", request=request),
        })


class PizzaListView(APIView):
    def get(self, request):
        pizza = Pizza.objects.all()
        serializer_context = {'request': request}
        serializer = PizzaSerializer(pizza,
                                     context=serializer_context,
                                     many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_context = {'request': request}
        serializer = PizzaSerializer(data=request.data,
                                     context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PizzaDetailView(APIView):
    def get(self, request, pk):
        pizza = get_object_or_404(Pizza, pk=pk)
        serializer_context = {'request': request}
        serializer = PizzaSerializer(pizza, context=serializer_context)
        return Response(serializer.data)

    def patch(self, request, pk):
        pizza = get_object_or_404(Pizza, pk=pk)
        serializer_context = {'request': request}
        serializer = PizzaSerializer(pizza,
                                     data=request.data,
                                     context=serializer_context,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VoteDetailView(APIView):
    def patch(self, request, pk):
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.votes += 1
        pizza.save()
        serializer_context = {'request': request}
        serializer = PizzaSerializer(pizza, context=serializer_context)
        return Response(serializer.data)


class ToppingsListView(APIView):
    def get(self, request):
        toppings = Topping.objects.all()
        serializer_context = {'request': request}
        serializer = ToppingsSerializer(toppings,
                                        context=serializer_context,
                                        many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer_context = {'request': request}
        serializer = ToppingsSerializer(data=request.data,
                                        context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToppingsDetailView(APIView):
    def get(self, request, pk):
        topping = get_object_or_404(Topping, pk=pk)
        serializer_context = {'request': request}
        serializer = ToppingsSerializer(topping, context=serializer_context)
        return Response(serializer.data)

    def put(self, request, pk):
        topping = get_object_or_404(Topping, pk=pk)
        serializer_context = {'request': request}
        serializer = ToppingsSerializer(topping,
                                        data=request.data,
                                        context=serializer_context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        topping = get_object_or_404(Topping, pk=pk)
        topping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
