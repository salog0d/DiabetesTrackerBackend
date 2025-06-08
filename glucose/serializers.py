from rest_framework import serializers
from .models import RangoGlucosaReferencia, MedicionGlucosa


class RangoGlucosaReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RangoGlucosaReferencia
        fields = '__all__'


class MedicionGlucosaSerializer(serializers.ModelSerializer):
    clasificacion = serializers.SerializerMethodField()
    es_alerta = serializers.ReadOnlyField()

    class Meta:
        model = MedicionGlucosa
        fields = '__all__'

    def get_clasificacion(self, obj):
        return obj.get_clasificacion()