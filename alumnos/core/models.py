from django.db import models
from django.contrib.auth.models import User

class Materia(models.Model):
    siglas = models.CharField(max_length=32, null=True)
    nombre = models.CharField(max_length=128, null=True)

    def __str__(self):
        return u'%s' % (self.nombre)

class Comision(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return u'%s' % (self.nombre)

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=2)

    def __str__(self):
        return u'%s' % (self.nombre)

class PlanDeEstudio(models.Model):
    nombre = models.CharField(max_length=64)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True)
    anio = models.CharField(max_length=4)

    def __str__(self):
        return u'%s' % (self.nombre)

class MateriaEnPlan(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanDeEstudio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=64)
    tipo = models.CharField(choices=(('b' ,'Basica'), ('a' ,'Avanzada'), ('o' ,'Optativa')), max_length=2)
    creditos = models.IntegerField(default=0)
    codigo = models.CharField(max_length=10)

    def __str__(self):
        return u'%s' % (self.nombre)

class Alumno(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=15)
    email = models.CharField(max_length=128)
    legajo = models.CharField(max_length=32)
    es_regular = models.BooleanField(default=True)
    sexo = models.CharField(choices=(('F', 'Femenino'), ('M', 'Masculino')), max_length=2)
    telefono = models.CharField(max_length=32, null=True)
    celular = models.CharField(max_length=32, null=True)
    tiene_beca = models.BooleanField(default=False)
    tiene_tutor = models.BooleanField(default=False)
    tiene_pc = models.BooleanField(default=False)
    tiene_pendrive = models.BooleanField(default=False)
    tiene_portatil = models.BooleanField(default=False)
    comentario = models.CharField(max_length=255, null=True)
    observacion = models.CharField(max_length=255, null=True)

    def __str__(self):
        return u'%s, %s' % (self.apellido, self.nombre)


class AlumnoDeCarrera(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanDeEstudio, on_delete=models.CASCADE)
    promedio = models.CharField(max_length=3, null=True)
    coeficiente = models.CharField(max_length=3, null=True)
    cuatrimestre_inscripto = models.CharField(max_length=8, null=True) #Cuatrimestre Ingreso

    def __str__(self):
        return u'%s-%s' % (self.alumno, self.carrera)

class MateriaCursada(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='cursadas')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='cursadas')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    comision = models.ForeignKey(Comision, null=True, on_delete=models.SET_NULL)
    nota = models.CharField(max_length=3, default='C', choices=(
                                ('C', 'Cursando'),
                                ('EQ', 'Equivalencia'),
                                ('AP', 'Aprobado'),
                                ('D', 'Desaprobado'),('1', '1'),('2', '2'),
                                ('3', '3'),('4', '4'),('5', '5'),('6', '6'),
                                ('7', '7'), ('8', '8'),('9', '9'),('10', '10')))
    anio = models.CharField(max_length=4)
    cuatrimestre = models.CharField(max_length=1, choices=(('1', 'C1'), ('2', 'C2')))

    def __str__(self):
        return u'%s, %s' % (self.comision.materia, self.alumno)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carreras = models.ManyToManyField(Carrera)

    def __str__(self):
        return u'%s' % self.user