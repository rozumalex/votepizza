from django.urls import path

from . import views


app_name = 'pizza'

urlpatterns = [
    path('', views.API.as_view(), name='api'),
    path('pizza/', views.PizzaListView.as_view(), name='pizza-list'),
    path('pizza/<pk>/', views.PizzaDetailView.as_view(),
         name='pizza-detail'),
    path('pizza/<pk>/vote/', views.VoteDetailView.as_view(),
         name='pizza-vote'),
    path('toppings/', views.ToppingsListView.as_view(),
         name='toppings-list'),
    path('toppings/<pk>/', views.ToppingsDetailView.as_view(),
         name='toppings-detail'),
]
