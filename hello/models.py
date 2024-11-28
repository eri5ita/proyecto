from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class misiones(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    leafpoints = models.IntegerField()
    def __str__(self):
        return self.titulo
    

class UsuarioLeafpoints(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Vincula a un usuario
    total_leafpoints = models.IntegerField(default=0)  # Puntos totales disponibles

    def __str__(self):
        return f"{self.usuario.username} - Leafpoints: {self.total_leafpoints}"

    # Señal para crear automáticamente un registro de UsuarioLeafpoints al crear un usuario
    @receiver(post_save, sender=User)
    def crear_leafpoints_usuario(sender, instance, created, **kwargs):
        if created:
            UsuarioLeafpoints.objects.create(usuario=instance)

    @receiver(post_save, sender=User)
    def guardar_leafpoints_usuario(sender, instance, **kwargs):
        instance.usuarioleafpoints.save()

class mision_completada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mision = models.ForeignKey(misiones, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('usuario', 'mision')
        
    def _str_(self):
        return f"{self.usuario.username} completó {self.mision.nombre}"


class recompensas(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    costo_lp = models.IntegerField()

    def __str__(self):
        return self.title

class RecompensaComprada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recompensas_compradas")
    recompensa = models.ForeignKey(recompensas, on_delete=models.CASCADE, related_name="compras")
    comprada = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'recompensa')  # Evita duplicados para una misma recompensa, usuario y misión

    def __str__(self):
        return f"{self.usuario.username} - {self.recompensa.title}"