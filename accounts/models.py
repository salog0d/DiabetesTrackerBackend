from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Modelo extendido de usuario usando AbstractUser de Django.
    Mejor práctica: extender User desde el inicio del proyecto.
    """
    
    class SexoChoices(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'
        OTRO = 'O', 'Otro'
    
    class NivelActividadChoices(models.TextChoices):
        SEDENTARIO = 'sedentario', 'Sedentario'
        LIGERO = 'ligero', 'Ligero'
        MODERADO = 'moderado', 'Moderado'
        INTENSO = 'intenso', 'Intenso'
    
    sexo = models.CharField(
        max_length=1, 
        choices=SexoChoices.choices, 
        null=True, 
        blank=True
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(999.99)]
    )
    estatura = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(3.0)]
    )
    nivel_actividad = models.CharField(
        max_length=20, 
        choices=NivelActividadChoices.choices,
        default=NivelActividadChoices.SEDENTARIO
    )
    estado = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)
    
    # Campos para evitar colisión con auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username}"
    
    @property
    def edad(self):
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
    
    @property
    def imc(self):
        if self.peso and self.estatura:
            return round(float(self.peso) / (float(self.estatura) ** 2), 2)
        return None


class SurveyInicial(models.Model):
    """
    Survey inicial único por usuario para personalización de la experiencia.
    Relación OneToOne garantiza un survey por usuario.
    """
    
    class TipoDiabetesChoices(models.TextChoices):
        TIPO1 = 'tipo1', 'Tipo 1'
        TIPO2 = 'tipo2', 'Tipo 2'
        GESTACIONAL = 'gestacional', 'Gestacional'
    
    class FrecuenciaEjercicioChoices(models.TextChoices):
        NUNCA = 'nunca', 'Nunca'
        SEMANAL = 'semanal', 'Semanal'
        DIARIO = 'diario', 'Diario'
        MULTIPLE_DIARIO = 'multiple_diario', 'Múltiple por día'
    
    class ConsumoAlcoholChoices(models.TextChoices):
        NUNCA = 'nunca', 'Nunca'
        OCASIONAL = 'ocasional', 'Ocasional'
        FRECUENTE = 'frecuente', 'Frecuente'
    
    class ObjetivoPrincipalChoices(models.TextChoices):
        CONTROL_GLUCOSA = 'control_glucosa', 'Control de Glucosa'
        PESO = 'peso', 'Control de Peso'
        EJERCICIO = 'ejercicio', 'Incrementar Ejercicio'
        GENERAL = 'general', 'Salud General'
    
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='survey_inicial'
    )
    
    tiene_diabetes = models.BooleanField(default=False)
    tipo_diabetes = models.CharField(
        max_length=15,
        choices=TipoDiabetesChoices.choices,
        null=True,
        blank=True
    )
    fecha_diagnostico = models.DateField(null=True, blank=True)
    medicamentos_actuales = models.TextField(blank=True)
    
    parentesco_diabetes = models.CharField(max_length=100, blank=True)
    
    frecuencia_ejercicio = models.CharField(
        max_length=20,
        choices=FrecuenciaEjercicioChoices.choices,
        default=FrecuenciaEjercicioChoices.NUNCA
    )
    habito_fumar = models.BooleanField(default=False)
    consumo_alcohol = models.CharField(
        max_length=20,
        choices=ConsumoAlcoholChoices.choices,
        default=ConsumoAlcoholChoices.NUNCA
    )
    
    objetivo_principal = models.CharField(
        max_length=20,
        choices=ObjetivoPrincipalChoices.choices,
        default=ObjetivoPrincipalChoices.GENERAL
    )
    meta_glucosa_promedio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(70), MaxValueValidator(300)]
    )
    
    fecha_completado = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'survey_inicial'
        verbose_name = 'Survey Inicial'
        verbose_name_plural = 'Surveys Iniciales'
    
    def __str__(self):
        return f"Survey Inicial - {self.usuario.get_full_name()}"
