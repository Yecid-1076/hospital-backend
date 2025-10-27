from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    ROLES = (
        ('director_medico', 'Director Médico'),
        ('enfermero_admin', 'Enfermero Administrador'),
        ('medico', 'Médico'),
        ('enfermero', 'Enfermero'),
        ('porteria', 'Portería'),
        ('paciente', 'Paciente'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='paciente')
    telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_rol_display()}"
    
    # Métodos de verificación de permisos
    def es_director_medico(self):
        return self.rol == 'director_medico'
    
    def es_enfermero_admin(self):
        return self.rol == 'enfermero_admin'
    
    def es_medico(self):
        return self.rol == 'medico'
    
    def es_enfermero(self):
        return self.rol == 'enfermero'
    
    def es_porteria(self):
        return self.rol == 'porteria'
    
    def es_paciente(self):
        return self.rol == 'paciente'
    
    # Métodos de permisos específicos
    def puede_gestionar_medicos(self):
        return self.rol in ['director_medico']
    
    def puede_gestionar_enfermeros(self):
        return self.rol in ['enfermero_admin']
    
    def puede_gestionar_porteria(self):
        return self.rol in ['enfermero_admin']
    
    def puede_ver_todas_citas(self):
        return self.rol in ['director_medico']
    
    def puede_gestionar_camas(self):
        return self.rol in ['enfermero_admin', 'enfermero']
    
    def puede_ver_historiales_completos(self):
        return self.rol in ['director_medico']
    
    def puede_registrar_acompanantes(self):
        return self.rol in ['porteria']

# Señales para crear perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfilusuario.save()