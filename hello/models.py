from django.db import models

# Create your models here.
class misiones(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.TextField(max_length=50)
    leafpoints = models.IntegerField()
    def __str__(self):
        return self.titulo
    
class recompensas(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    costo_lp = models.IntegerField()