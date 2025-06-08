from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, SurveyInicial
from .serializers import (
    UserSerializer,
    SurveyInicialSerializer,
    CustomTokenObtainPairSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  


class SurveyInicialViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyInicialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SurveyInicial.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        if SurveyInicial.objects.filter(usuario=self.request.user).exists():
            raise PermissionDenied("Ya existe un survey para este usuario.")
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.usuario != self.request.user:
            raise PermissionDenied("No puedes modificar el survey de otro.")
        serializer.save()
