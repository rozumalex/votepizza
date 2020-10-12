from django.conf.urls import url

from . import views


app_name = 'pizza'

urlpatterns = [
    url(r'^pizza/$',
        views.PizzaListView.as_view(),
        name='pizza-list'),
    url(r'^pizza/(?P<pk>\d+)/$',
        views.PizzaDetailView.as_view(),
        name='pizza-detail'),
    url(r'^pizza/(?P<pk>\d+)/vote/$', views.VoteDetailView.as_view(),
        name='pizza-vote'),
    url(r'^pizza/(?P<pk>\d+)/(?P<topping_pk>\d+)/$',
        views.ToppingsInPizzaDetailView.as_view(),
        name='toppings-in-pizza'),
    url(r'^toppings/$',
        views.ToppingsListView.as_view(),
        name='toppings-list'),
    url(r'^toppings/(?P<pk>\d+)/$',
        views.ToppingsDetailView.as_view(),
        name='toppings-detail'),
]
