from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


from .models import Pizza, Topping
from .serializers import PizzaSerializer, ToppingSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer


class PizzaVoteView(APIView):
    # authentication_classes = (BasicAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def patch(self, request, pk, format=None):
        pizza = get_object_or_404(Pizza, pk=pk)
        pizza.votes += 1
        pizza.save()
        return Response({'voted': True})
