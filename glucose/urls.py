from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RangoGlucosaReferenciaViewSet, MedicionGlucosaViewSet

router = DefaultRouter()
router.register(r'rangos-glucosa', RangoGlucosaReferenciaViewSet, basename='rangos-glucosa')
router.register(r'mediciones-glucosa', MedicionGlucosaViewSet, basename='mediciones-glucosa')

urlpatterns = [
    path('', include(router.urls)),
]