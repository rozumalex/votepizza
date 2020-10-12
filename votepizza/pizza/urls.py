from django.conf.urls import url, include
from rest_framework import routers

from . import views


app_name = 'pizza'

router = routers.DefaultRouter()
router.register('pizza', views.PizzaViewSet)
router.register('toppings', views.ToppingViewSet)

urlpatterns = [
    url(r'^pizza/(?P<pk>\d+)/vote/$', views.PizzaVoteView.as_view(),
        name='pizza-vote'),
    url(r'^', include(router.urls)),
]
