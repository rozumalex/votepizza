from rest_framework import generics
from rest_framework.views import APIView
from django.http.response import HttpResponseRedirect
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.response import Response

from .models import Pizza, Topping
from .serializers import PizzaSerializer, ToppingsSerializer, VoteSerializer


class APIRootView(APIView):
    def get(self, request):
        return Response({
            'pizza': reverse("pizza:pizza-list", request=request),
            'toppings': reverse("pizza:toppings-list", request=request),
        })


class PizzaListView(generics.ListCreateAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class PizzaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class VoteForPizzaView(generics.UpdateAPIView):
    queryset = Pizza.objects.all()
    serializer_class = VoteSerializer

    def patch(self, request, *args, **kwargs):
        pizza = self.get_object()
        pizza.votes += 1
        pizza.save()
        return HttpResponseRedirect(reverse_lazy('pizza:pizza-detail',
                                                 args=[pizza.id]))


class ToppingsListView(generics.ListCreateAPIView):
    queryset = Topping.objects.all()
    serializer_class = ToppingsSerializer


class ToppingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topping.objects.all()
    serializer_class = ToppingsSerializer
