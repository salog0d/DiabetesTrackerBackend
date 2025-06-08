
from django.core.cache import cache
from .models import ConfiguracionSistema

class ConfiguracionUtils:
    '''
    Utilidades para acceso eficiente a configuración.
    Implementa patrón Cache-Aside para performance.
    
    Nota: Con acceso democrático, la configuración puede cambiar frecuentemente,
    por lo que el cache tiene TTL más corto y se invalida automáticamente.
    '''
    
    @staticmethod
    def get_cached_config():
        '''
        Obtener configuración con cache.
        TTL reducido debido a cambios más frecuentes por múltiples usuarios.
        '''
        config = cache.get('sistema_configuracion')
        if config is None:
            config = ConfiguracionSistema.get_instance()
            cache.set('sistema_configuracion', config, 180)  # 3 minutos (reducido)
        return config
    
    @staticmethod
    def is_hipoglucemia(valor_glucosa):
        '''Verificar si valor indica hipoglucemia según configuración actual.'''
        config = ConfiguracionUtils.get_cached_config()
        return valor_glucosa < config.umbral_hipoglucemia
    
    @staticmethod
    def is_hiperglucemia(valor_glucosa):
        '''Verificar si valor indica hiperglucemia según configuración actual.'''
        config = ConfiguracionUtils.get_cached_config()
        return valor_glucosa > config.umbral_hiperglucemia
    
    @staticmethod
    def get_status_glucosa(valor_glucosa):
        '''
        Obtener estado de glucosa (normal/hipo/hiper).
        
        Returns:
            str: 'hipoglucemia', 'hiperglucemia', 'normal'
        '''
        if ConfiguracionUtils.is_hipoglucemia(valor_glucosa):
            return 'hipoglucemia'
        elif ConfiguracionUtils.is_hiperglucemia(valor_glucosa):
            return 'hiperglucemia'
        else:
            return 'normal'
    
    @staticmethod
    def get_status_with_details(valor_glucosa):
        '''
        Obtener estado detallado de glucosa con información de umbrales.
        
        Returns:
            dict: Información completa del estado de glucosa
        '''
        config = ConfiguracionUtils.get_cached_config()
        status = ConfiguracionUtils.get_status_glucosa(valor_glucosa)
        
        return {
            'valor': valor_glucosa,
            'status': status,
            'umbral_hipoglucemia': float(config.umbral_hipoglucemia),
            'umbral_hiperglucemia': float(config.umbral_hiperglucemia),
            'en_rango_normal': status == 'normal',
            'requiere_atencion': status != 'normal',
            'diferencia_umbral_inferior': valor_glucosa - float(config.umbral_hipoglucemia),
            'diferencia_umbral_superior': float(config.umbral_hiperglucemia) - valor_glucosa,
            'configuracion_actualizada': config.fecha_actualizacion
        }
    
    @staticmethod
    def invalidate_cache():
        '''Invalidar cache de configuración manualmente.'''
        cache.delete('sistema_configuracion')
    
    @staticmethod
    def get_recordatorio_info():
        '''Obtener información de configuración de recordatorios.'''
        config = ConfiguracionUtils.get_cached_config()
        return {
            'medicion_horas': config.recordatorio_medicion_horas,
            'comida_horas': config.recordatorio_comida_horas,
            'mediciones_por_dia': 24 // config.recordatorio_medicion_horas,
            'recordatorios_comida_por_dia': 24 // config.recordatorio_comida_horas,
            'configuracion_actualizada': config.fecha_actualizacion
        }