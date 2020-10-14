from rest_framework import generics
from rest_framework.views import APIView

from django.http.response import HttpResponseNotAllowed
from rest_framework.reverse import reverse
from rest_framework.response import Response
import datetime
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin

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


class PatchOnlyMixin(object):
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


class VoteForPizzaView(PatchOnlyMixin, UpdateModelMixin,
                       generics.GenericAPIView):
    queryset = Pizza.objects.all()
    serializer_class = VoteSerializer

    def patch(self, request, *args, **kwargs):
        pizza = self.get_object()
        if request.COOKIES.get('voted', None):
            return Response({'error': 'You have already voted'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            pizza.votes += 1
            pizza.save()
            response = Response({'votes': pizza.votes})
            expires = datetime.datetime.strftime(
                datetime.datetime.utcnow() + datetime.timedelta(seconds=15),
                '%a, %d-%b-%Y %H:%M:%S GMT')
            response.set_cookie(key='voted', value=True,
                                max_age=15, expires=expires)
        return response

    def update(self, request, *args, **kwargs):
        return HttpResponseNotAllowed()


class ToppingsListView(generics.ListCreateAPIView):
    queryset = Topping.objects.all()
    serializer_class = ToppingsSerializer


class ToppingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topping.objects.all()
    serializer_class = ToppingsSerializer
