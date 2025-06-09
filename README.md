# DiabetesTracker

**Sistema integral de seguimiento y gestión de diabetes basado en Django REST Framework**

[![Django](https://img.shields.io/badge/Django-5.2.2-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST-3.16.0-red?style=flat)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=flat&logo=jsonwebtokens)](https://jwt.io/)

## Descripción

DiabetesTracker es una plataforma completa diseñada para el monitoreo personalizado de diabetes, que combina seguimiento de glucosa, gestión nutricional avanzada y análisis predictivo. El sistema implementa patrones de diseño empresariales y mejores prácticas de desarrollo para ofrecer una solución escalable y mantenible.

### Características Principales

- **Gestión de Usuarios Personalizada**: Sistema de autenticación extendido con perfiles médicos detallados
- **Monitoreo de Glucosa**: Tracking inteligente con alertas automáticas y análisis de tendencias
- **Sistema Nutricional Avanzado**: Catálogo completo de alimentos con índices glucémicos y análisis calórico
- **Configuración Dinámica**: Sistema centralizado de configuraciones con cache inteligente
- **API RESTful Completa**: Endpoints documentados con autenticación JWT
- **Arquitectura Modular**: Diseño escalable con separación clara de responsabilidades

## Arquitectura del Sistema

### Estructura Modular

```
DiabetesTracker/
├── accounts/          # Gestión de usuarios y autenticación
├── core/             # Configuraciones centrales y utilidades
├── glucose/          # Monitoreo de glucosa y alertas
├── nutrition/        # Sistema nutricional y alimentos
└── DiabetesTracker/  # Configuración principal del proyecto
```

### Patrones de Diseño Implementados

**Singleton Pattern**: Configuración global del sistema en `core.models.ConfiguracionSistema`
- Garantiza una única instancia de configuración
- Cache inteligente con invalidación automática
- Acceso thread-safe a configuraciones críticas

**Repository Pattern**: Separación de lógica de negocio y acceso a datos
- ViewSets especializados para cada entidad
- Filtrado automático por usuario en QuerySets
- Serializers con validaciones de negocio

**Strategy Pattern**: Sistema flexible de clasificación nutricional
- Múltiples estrategias de análisis de alimentos
- Cálculos dinámicos de índices glucémicos
- Algoritmos intercambiables de recomendaciones

## Módulos del Sistema

### Accounts
**Gestión completa de usuarios y autenticación**

Funcionalidades principales:
- Usuario extendido con campos médicos específicos
- Sistema de autenticación JWT con refresh tokens
- Survey inicial para personalización de experiencia
- Cálculo automático de IMC y edad
- Perfiles de actividad física personalizables

Modelos clave:
- `User`: Extensión de AbstractUser con datos médicos
- `SurveyInicial`: Cuestionario de onboarding personalizado

### Core
**Sistema central de configuraciones y utilidades**

Funcionalidades principales:
- Configuración global del sistema con patrón Singleton
- Utilidades de cache con TTL optimizado
- Sistema de alertas configurables
- Análisis automático de estados de glucosa
- Gestión centralizada de umbrales médicos

Componentes clave:
- `ConfiguracionSistema`: Configuraciones globales
- `ConfiguracionUtils`: Utilidades con cache inteligente

### Glucose
**Monitoreo inteligente de niveles de glucosa**

Funcionalidades principales:
- Registro de mediciones con timestamps precisos
- Sistema de alertas automáticas
- Clasificación automática de estados glucémicos
- Análisis de tendencias y patrones
- Rangos de referencia personalizables

### Nutrition
**Sistema avanzado de gestión nutricional**

Funcionalidades principales:
- Catálogo extenso de tipos de alimentos
- Índices glucémicos y valores nutricionales
- Registro detallado de comidas por horarios
- Cálculos automáticos de calorías
- Análisis de impacto glucémico de alimentos
- Sistema de conversión de unidades de medida

Modelos principales:
- `TipoAlimento`: Catálogo maestro con datos nutricionales
- `Comida`: Registro de comidas con análisis temporal
- `DetalleComida`: Composición específica de cada comida

## Instalación y Configuración

### Prerrequisitos

```bash
Python 3.8+
Django 5.2.2
PostgreSQL 12+ (recomendado) o SQLite para desarrollo
```

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/diabetes-tracker.git
cd diabetes-tracker
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
```bash
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://usuario:password@localhost:5432/diabetes_tracker
ALLOWED_HOSTS=localhost,127.0.0.1
```

## API Endpoints

### Autenticación

```http
POST /api/token/                    # Obtener token de acceso
POST /api/token/refresh/            # Renovar token
```

### Usuarios

```http
GET    /api/usuarios/               # Listar usuarios
POST   /api/usuarios/               # Crear usuario
GET    /api/usuarios/{id}/          # Detalle de usuario
PUT    /api/usuarios/{id}/          # Actualizar usuario
DELETE /api/usuarios/{id}/          # Eliminar usuario
```

### Survey Inicial

```http
GET    /api/survey-inicial/         # Obtener survey del usuario
POST   /api/survey-inicial/         # Crear survey inicial
PUT    /api/survey-inicial/{id}/    # Actualizar survey
```

### Configuración

```http
GET    /configuracion/              # Obtener configuración global
PUT    /configuracion/              # Actualizar configuración
```

### Nutrición

```http
GET    /tipos-alimentos/            # Catálogo de alimentos
POST   /tipos-alimentos/            # Crear tipo de alimento
GET    /comidas/                    # Historial de comidas del usuario
POST   /comidas/                    # Registrar nueva comida
GET    /detalles-comida/            # Detalles de composición
```

### Glucosa

```http
GET    /rangos-glucosa/             # Rangos de referencia
GET    /mediciones-glucosa/         # Historial de mediciones
POST   /mediciones-glucosa/         # Nueva medición
```

## Estructura de Datos

### Modelo de Usuario Extendido

```python
{
    "id": 1,
    "username": "usuario123",
    "email": "usuario@email.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "sexo": "M",
    "fecha_nacimiento": "1985-06-15",
    "peso": 75.50,
    "estatura": 1.75,
    "nivel_actividad": "moderado",
    "edad": 38,
    "imc": 24.65
}
```

### Registro de Comida

```python
{
    "id": 1,
    "tipo_comida": "desayuno",
    "fecha_hora": "2025-06-08T08:30:00Z",
    "calorias_totales": 450.75,
    "indice_glucemico_promedio": 65.30,
    "detalles": [
        {
            "tipo_alimento": 1,
            "cantidad": 2,
            "unidad_medida": "piezas"
        }
    ]
}
```

## Características Técnicas Avanzadas

### Sistema de Cache Inteligente

El sistema implementa cache estratégico en múltiples niveles:

**Cache de Configuración**: Las configuraciones globales se cachean con TTL optimizado y invalidación automática
**Cache de Consultas**: QuerySets frecuentes se almacenan temporalmente
**Cache de Cálculos**: Resultados de cálculos complejos (IMC, análisis glucémicos) se mantienen en memoria

### Validaciones de Negocio

**Validación de Rangos Médicos**: Todos los valores de glucosa, peso y medidas se validan contra rangos médicamente aceptables
**Integridad Referencial**: Constraints de base de datos garantizan consistencia de datos
**Validación Temporal**: Verificación de secuencias lógicas en timestamps de mediciones

### Optimizaciones de Performance

**Select Related**: Uso estratégico de `select_related()` y `prefetch_related()`
**Índices de Base de Datos**: Índices compuestos en campos frecuentemente consultados
**Paginación Inteligente**: Paginación automática en endpoints con grandes volúmenes de datos

## Seguridad

### Autenticación y Autorización

- **JWT Tokens**: Implementación segura con refresh tokens
- **Rotación de Tokens**: Tokens se rotan automáticamente para mayor seguridad
- **Blacklisting**: Sistema de invalidación de tokens comprometidos
- **Permisos Granulares**: Control de acceso por usuario y recurso

### Protección de Datos

- **Filtrado Automático**: Los usuarios solo acceden a sus propios datos
- **Validación de Input**: Sanitización y validación exhaustiva de entrada
- **Logs de Auditoría**: Tracking de operaciones críticas con timestamps

## Contribución

### Flujo de Desarrollo

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit con mensajes descriptivos
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request con descripción detallada

## Roadmap

### Versión 2.0 (Próximamente)

- **Análisis Predictivo**: Machine Learning para predicción de tendencias
- **Integración IoT**: Conectividad con dispositivos médicos
- **Dashboard Avanzado**: Visualizaciones interactivas con D3.js
- **Notificaciones Push**: Sistema de alertas en tiempo real
- **API GraphQL**: Endpoint GraphQL complementario
- **Aplicación Móvil**: Cliente nativo iOS/Android

## Reconocimientos

- Django REST Framework por el excelente framework
- Comunidad médica por feedback y validación
- Contribuidores del proyecto por mejoras continuas

---
