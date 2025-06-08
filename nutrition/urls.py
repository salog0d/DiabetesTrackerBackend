from rest_framework.routers import DefaultRouter
from .views import TipoAlimentoViewSet, ComidaViewSet, DetalleComidaViewSet

router = DefaultRouter()
router.register(r'tipos-alimentos', TipoAlimentoViewSet)
router.register(r'comidas', ComidaViewSet)
router.register(r'detalles-comida', DetalleComidaViewSet)

urlpatterns = router.urls
