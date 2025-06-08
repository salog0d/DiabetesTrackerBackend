from rest_framework import viewsets, permissions
from .models import RangoGlucosaReferencia, MedicionGlucosa
from .serializers import RangoGlucosaReferenciaSerializer, MedicionGlucosaSerializer
from rest_framework.permissions import IsAuthenticated


class RangoGlucosaReferenciaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RangoGlucosaReferencia.objects.all()
    serializer_class = RangoGlucosaReferenciaSerializer
    permission_classes = [permissions.IsAuthenticated]


class MedicionGlucosaViewSet(viewsets.ModelViewSet):
    serializer_class = MedicionGlucosaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MedicionGlucosa.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
