from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ConfiguracionSistema
from .serializers import ConfiguracionSistemaSerializer

class ConfiguracionSistemaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        config = ConfiguracionSistema.get_instance()
        serializer = ConfiguracionSistemaSerializer(config)
        return Response(serializer.data)

    def put(self, request):
        config = ConfiguracionSistema.get_instance()
        serializer = ConfiguracionSistemaSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
