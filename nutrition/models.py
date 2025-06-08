from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class TipoAlimento(models.Model):
    """
    Catálogo de tipos de alimentos con características nutricionales.
    Tabla maestra para normalización de datos alimentarios.
    """
    
    class CategoriaChoices(models.TextChoices):
        PROTEINA = 'proteina', 'Proteína'
        CARBOHIDRATO = 'carbohidrato', 'Carbohidrato'
        GRASA = 'grasa', 'Grasa'
        VERDURA = 'verdura', 'Verdura'
        FRUTA = 'fruta', 'Fruta'
        LACTEO = 'lacteo', 'Lácteo'
        OTRO = 'otro', 'Otro'
    
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(
        max_length=20,
        choices=CategoriaChoices.choices
    )
    indice_glucemico = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Índice glucémico del alimento (0-100)"
    )
    calorias_por_100g = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tipos_alimentos'
        verbose_name = 'Tipo de Alimento'
        verbose_name_plural = 'Tipos de Alimentos'
        ordering = ['categoria', 'nombre']
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['indice_glucemico']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"
    
    @property
    def impacto_glucemico(self):
        """Clasifica el impacto glucémico del alimento"""
        if not self.indice_glucemico:
            return 'No definido'
        
        if self.indice_glucemico <= 55:
            return 'Bajo'
        elif self.indice_glucemico <= 70:
            return 'Medio'
        else:
            return 'Alto'


class Comida(models.Model):
    """
    Registro de comidas realizadas por el usuario.
    Tabla principal para el tracking alimentario.
    """
    
    class TipoComidaChoices(models.TextChoices):
        DESAYUNO = 'desayuno', 'Desayuno'
        ALMUERZO = 'almuerzo', 'Almuerzo'
        CENA = 'cena', 'Cena'
        SNACK = 'snack', 'Snack'
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comidas'
    )
    tipo_comida = models.CharField(
        max_length=20,
        choices=TipoComidaChoices.choices
    )
    fecha_hora = models.DateTimeField()
    calorias_totales = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    notas = models.TextField(blank=True)
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comidas'
        verbose_name = 'Comida'
        verbose_name_plural = 'Comidas'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['usuario', '-fecha_hora']),
            models.Index(fields=['tipo_comida']),
            models.Index(fields=['fecha_hora']),
        ]
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_tipo_comida_display()} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"
    
    def calcular_calorias_totales(self):
        """
        Calcula automáticamente las calorías totales basadas en los detalles.
        Método de negocio en el modelo.
        """
        total = sum([
            detalle.calcular_calorias() 
            for detalle in self.detalles.all()
        ])
        self.calorias_totales = total
        return total
    
    @property
    def indice_glucemico_promedio(self):
        """Calcula el índice glucémico promedio ponderado de la comida"""
        detalles = self.detalles.select_related('tipo_alimento')
        total_peso = 0
        suma_ponderada = 0
        
        for detalle in detalles:
            if detalle.tipo_alimento.indice_glucemico:
                peso = float(detalle.cantidad_gramos)
                ig = float(detalle.tipo_alimento.indice_glucemico)
                suma_ponderada += peso * ig
                total_peso += peso
        
        return round(suma_ponderada / total_peso, 2) if total_peso > 0 else None


class DetalleComida(models.Model):
    """
    Detalle específico de alimentos en cada comida.
    Tabla de detalle que implementa relación muchos-a-muchos con atributos.
    """
    
    class UnidadMedidaChoices(models.TextChoices):
        GRAMOS = 'gramos', 'Gramos'
        PIEZAS = 'piezas', 'Piezas'
        TAZAS = 'tazas', 'Tazas'
        CUCHARADAS = 'cucharadas', 'Cucharadas'
        MILILITROS = 'ml', 'Mililitros'
    
    comida = models.ForeignKey(
        Comida,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    tipo_alimento = models.ForeignKey(
        TipoAlimento,
        on_delete=models.CASCADE,
        related_name='usos_en_comidas'
    )
    cantidad = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    unidad_medida = models.CharField(
        max_length=20,
        choices=UnidadMedidaChoices.choices
    )
    
    class Meta:
        db_table = 'detalle_comidas'
        verbose_name = 'Detalle de Comida'
        verbose_name_plural = 'Detalles de Comidas'
        unique_together = ['comida', 'tipo_alimento']  # Evita duplicados en la misma comida
    
    def __str__(self):
        return f"{self.cantidad} {self.unidad_medida} de {self.tipo_alimento.nombre}"
    
    @property
    def cantidad_gramos(self):
        """
        Convierte la cantidad a gramos para cálculos uniformes.
        Implementa conversiones básicas de unidades.
        """
        conversion_factor = {
            'gramos': 1,
            'piezas': 100,  # Estimación promedio
            'tazas': 250,   # Estimación promedio
            'cucharadas': 15,  # Estimación estándar
            'ml': 1,  # Para líquidos, similar peso
        }
        
        factor = conversion_factor.get(self.unidad_medida, 1)
        return float(self.cantidad) * factor
    
    def calcular_calorias(self):
        """Calcula las calorías de este detalle específico"""
        if self.tipo_alimento.calorias_por_100g:
            gramos = self.cantidad_gramos
            calorias_por_gramo = float(self.tipo_alimento.calorias_por_100g) / 100
            return round(gramos * calorias_por_gramo, 2)
        return 0
