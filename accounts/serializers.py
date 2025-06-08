# serializers.py

from rest_framework import serializers
from .models import User, SurveyInicial
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extiende el token para devolver datos extra del usuario."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agrega campos personalizados al token si deseas
        token['username'] = user.username
        token['email'] = user.email
        token['es_activo'] = user.activo
        return token


class UserSerializer(serializers.ModelSerializer):
    edad = serializers.ReadOnlyField()
    imc = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'sexo',
            'fecha_nacimiento', 'peso', 'estatura', 'nivel_actividad',
            'estado', 'activo', 'edad', 'imc'
        ]


class SurveyInicialSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SurveyInicial
        fields = '__all__'
