from django.db import models


class ConfiguracionSistema(models.Model):
    """
    Configuraciones globales del sistema.
    Patrón Singleton para configuraciones centralizadas.
    """
    
    # Configuraciones de alertas
    umbral_hipoglucemia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=70.00,
        help_text="Umbral para alertas de hipoglucemia (mg/dL)"
    )
    umbral_hiperglucemia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=200.00,
        help_text="Umbral para alertas de hiperglucemia (mg/dL)"
    )
    
    # Configuraciones de recordatorios
    recordatorio_medicion_horas = models.PositiveIntegerField(
        default=8,
        help_text="Intervalo en horas para recordatorios de medición"
    )
    recordatorio_comida_horas = models.PositiveIntegerField(
        default=6,
        help_text="Intervalo en horas para recordatorios de registro de comida"
    )
    
    # Metadata
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'configuracion_sistema'
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
    
    def save(self, *args, **kwargs):
        """Implementa patrón Singleton"""
        if not self.pk and ConfiguracionSistema.objects.exists():
            raise ValueError('Solo puede existir una configuración del sistema')
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_instance(cls):
        """Método de clase para obtener la instancia única"""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'umbral_hipoglucemia': 70.00,
                'umbral_hiperglucemia': 200.00,
            }
        )
        return obj
    
    def __str__(self):
        return f"Configuración del Sistema (Actualizada: {self.fecha_actualizacion.strftime('%d/%m/%Y')})"