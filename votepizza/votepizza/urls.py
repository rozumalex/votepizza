from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Pastebin API')


urlpatterns = [
    url(r'^api/$', schema_view),
    url(r'^api/', include('pizza.urls', namespace='pizza')),
    path('admin/', admin.site.urls),
]
