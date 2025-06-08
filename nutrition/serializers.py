from rest_framework import serializers
from .models import TipoAlimento, Comida, DetalleComida


class TipoAlimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAlimento
        fields = '__all__'


class DetalleComidaSerializer(serializers.ModelSerializer):
    tipo_alimento_nombre = serializers.CharField(source='tipo_alimento.nombre', read_only=True)

    class Meta:
        model = DetalleComida
        fields = '__all__'


class ComidaSerializer(serializers.ModelSerializer):
    detalles = DetalleComidaSerializer(many=True, read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    indice_glucemico_promedio = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Comida
        fields = '__all__'
