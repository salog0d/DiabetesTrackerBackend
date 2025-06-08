# alimentos/views.py
from rest_framework import viewsets, permissions
from .models import TipoAlimento, Comida, DetalleComida
from .serializers import TipoAlimentoSerializer, ComidaSerializer, DetalleComidaSerializer


class TipoAlimentoViewSet(viewsets.ModelViewSet):
    queryset = TipoAlimento.objects.all()
    serializer_class = TipoAlimentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComidaViewSet(viewsets.ModelViewSet):
    serializer_class = ComidaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comida.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class DetalleComidaViewSet(viewsets.ModelViewSet):
    serializer_class = DetalleComidaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DetalleComida.objects.filter(comida__usuario=self.request.user)
