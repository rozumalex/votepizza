from django.urls import path

from . import views


app_name = 'pizza'

urlpatterns = [
    path(r'^/$', views.API.as_view(), name='api'),
    path(r'^pizza/$', views.PizzaListView.as_view(), name='pizza-list'),
    path(r'^pizza/(?P<pk>\d+)/$', views.PizzaDetailView.as_view(),
         name='pizza-detail'),
    path(r'^pizza/(?P<pk>\d+)/vote/$', views.VoteDetailView.as_view(),
         name='pizza-vote'),
    path(r'^toppings/$', views.ToppingsListView.as_view(),
         name='toppings-list'),
    path(r'^toppings/(?P<pk>\d+)/$', views.ToppingsDetailView.as_view(),
         name='toppings-detail'),
]
