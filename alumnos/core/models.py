from django.db import models

class Materia(models.Model):
    siglas = models.CharField(max_length=32)

    def __str__(self):
        return u'%s' % (self.siglas)

class Comision(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return u'%s' % (self.nombre)

class MateriaEnPlan(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=64)
    tipo = models.CharField(choices=(('b' ,'Basica'), ('a' ,'Avanzada'), ('o' ,'Optativa')), max_length=2)
    creditos = models.IntegerField()

    def __str__(self):
        return u'%s' % (self.nombre)

class PlanDeEstudio(models.Model):
    nombre = models.CharField(max_length=64)
    materias = models.ManyToManyField(Materia)

    def __str__(self):
        return u'%s' % (self.nombre)

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    planes = models.ManyToManyField(PlanDeEstudio)

    def __str__(self):
        return u'%s' % (self.nombre)

class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.CharField(max_length=15)

    def __str__(self):
        return u'%s, %s' % (self.apellido, self.nombre)

class Alumno(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    legajo = models.CharField(max_length=32)
    carreras = models.ManyToManyField(Carrera)
    es_regular = models.BooleanField(default=True)
    sexo = models.CharField(choices=(('F', 'Femenino'), ('M', 'Masculino')), max_length=2)
    cuatrimestre_inscripto = models.CharField(max_length=8, null=True)
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
        return u'%s' % (self.persona)

class Profesor(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=64)

    def __str__(self):
        return u'%s' % (self.persona)

class MateriaCursada(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    nota = models.CharField(max_length=3, choices=(
                                ('EQ', 'Equivalencia'), ('A', 'Aprobado'),
                                ('D', 'Desaprobado'),('1', '1'),('2', '2'),
                                ('3', '3'),('4', '4'),('5', '5'),('6', '6'),
                                ('7', '7'), ('8', '8'),('9', '9'),('10', '10')))

    def __str__(self):
        return u'%s, %s' % (self.materia, self.alumno)

class Inscripcion(models.Model):
    """
        TODO: Tendria que ver como guardar un historial
    """
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s, %s' % (self.materia, self.alumno)
