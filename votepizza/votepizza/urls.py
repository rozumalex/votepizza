from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Pastebin API')


urlpatterns = [
    path(r'^/$', schema_view),
    path(r'^api/', include('pizza.urls', namespace='pizza')),
    path('admin/', admin.site.urls),
]
