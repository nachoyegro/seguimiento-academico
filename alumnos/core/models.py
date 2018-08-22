from django.db import models

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)

class PlanDeEstudio(models.Model):
    nombre = models.CharField(max_length=64)
    carreras = models.ManyToManyField(Carrera)

class Alumno(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=15)
    legajo = models.CharField(max_length=8)
    carreras = models.ManyToManyField(Carrera)

class Materia(models.Model):
    nombre = models.CharField(max_length=255)
    carreras = models.ManyToManyField(Carrera)

class Inscripcion(models.Model):
    """
        TODO: Tendria que ver como guardar un historial
    """
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
