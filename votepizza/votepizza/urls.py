from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('pizza.urls', namespace='pizza')),
    path('admin/', admin.site.urls),
]
