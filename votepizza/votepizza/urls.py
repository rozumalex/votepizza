from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_swagger.views import get_swagger_view


swagger_pattern = [
    path('api/', include('pizza.urls', namespace='pizza')),
]

schema_view = get_swagger_view(title='Pastebin API', patterns=swagger_pattern)

urlpatterns = [
    path('', schema_view, name='site_root'),
    path('api/', include('pizza.urls', namespace='pizza')),
    path('admin/', admin.site.urls),
]
