from django.urls import path
from .views import ConfiguracionSistemaView

urlpatterns = [
    path('configuracion/', ConfiguracionSistemaView.as_view(), name='configuracion-sistema'),
]
