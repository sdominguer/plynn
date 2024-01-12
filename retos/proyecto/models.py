from django.db import models


# Create your models here.
class Calificacion(models.Model):
    idCalificacion = models.AutoField(primary_key=True)
    reto = models.CharField(max_length=255)
    promedioFactible = models.FloatField()
    promedioEstrategico = models.FloatField()
    grupo = models.CharField(max_length=150)

    @property
    def nota(self):
        # Calcula el promedio entre promedioFactible y promedioEstrategico
        return (self.promedioFactible + self.promedioEstrategico) / 2
