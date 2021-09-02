from django.db import models
from django.contrib.auth.models import User


class Materia(models.Model):
    siglas = models.CharField(max_length=32, null=True, blank=True)
    nombre = models.CharField(max_length=128, null=True, blank=True)
    codigo = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return u'%s' % (self.nombre)


class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=2)
    fecha_creacion = models.DateField(null=True, blank=True)

    def __str__(self):
        return u'%s' % (self.nombre)


class Area(models.Model):
    nombre = models.CharField(max_length=32)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s' % (self.nombre)


class Ciclo(models.Model):
    nombre = models.CharField(max_length=32)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s' % (self.nombre)


class PlanDeEstudio(models.Model):
    nombre = models.CharField(max_length=64)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True, blank=True)
    anio = models.IntegerField(verbose_name="Año")
    materias_necesarias = models.IntegerField(default=40)

    class Meta:
        verbose_name_plural = "Planes de estudio"

    def __gt__(self, other):
        return self.anio > other.anio

    def __str__(self):
        return u'%s' % (self.nombre)


class MateriaEnPlan(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanDeEstudio, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    ciclo = models.ForeignKey(Ciclo, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_en_plan = models.CharField(max_length=64)
    nucleo = models.CharField(choices=(('I', 'Introductoria'), ('B', 'Basica'), (
        'A', 'Avanzada'), ('C', 'Complementaria')), max_length=2, null=True, blank=True)
    creditos = models.IntegerField(null=True, blank=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    orden_cuatrimestral = models.IntegerField(null=True, blank=True)
    obligatorias = models.ManyToManyField(
        "self", related_name="obligatoria_de", symmetrical=False, blank=True)
    recomendadas = models.ManyToManyField(
        "self", related_name="recomendada_de", symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = "Materias de plan"

    def cantidad_obligatoria_de(self):
        acum = self.obligatoria_de.count()
        for materia in self.obligatoria_de.all():
            acum += materia.cantidad_obligatoria_de()
        return acum

    def __str__(self):
        return u'%s-%s' % (self.plan, self.materia)


class Alumno(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    dni = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    legajo = models.CharField(max_length=32)
    es_regular = models.BooleanField(default=True)
    sexo = models.CharField(
        choices=(('F', 'Femenino'), ('M', 'Masculino'), ('X', 'No binario')), max_length=2, null=True, blank=True)
    telefono = models.CharField(max_length=32, null=True, blank=True)
    celular = models.CharField(max_length=32, null=True, blank=True)
    tiene_beca = models.BooleanField(default=False)
    tiene_tutor = models.BooleanField(default=False)
    tiene_pc = models.BooleanField(default=False)
    tiene_pendrive = models.BooleanField(default=False)
    tiene_portatil = models.BooleanField(default=False)
    comentario = models.CharField(max_length=255, null=True, blank=True)
    observacion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return u'%s' % (self.legajo)


class AlumnoDeCarrera(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        PlanDeEstudio, on_delete=models.SET_NULL, null=True, blank=True)
    promedio = models.CharField(max_length=3, null=True, blank=True)
    coeficiente = models.CharField(max_length=3, null=True, blank=True)
    fecha_inscripcion = models.DateField(null=True, blank=True)

    def __str__(self):
        return u'%s-%s' % (self.alumno, self.carrera)


class MateriaCursada(models.Model):
    alumno = models.ForeignKey(
        Alumno, on_delete=models.CASCADE, related_name='cursadas')
    carrera = models.ForeignKey(
        Carrera, on_delete=models.CASCADE, related_name='cursadas')
    materia = models.ForeignKey(MateriaEnPlan, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=2, choices=(
        ('A', 'A- Aprobado'),
        ('E', 'E- Pendiente de Aprobacion'),
        ('N', 'N- Reprobado'),
        ('P', 'P- Aprobado'),
        ('U', 'U- Ausente'),
        ('R', 'R- Reprobado'),
        ('V', 'V- Pendiente Virtual'),
        ('', 'Ausente de Examen'),
    ), null=True, blank=True)
    nota = models.CharField(max_length=3, choices=(
        ('PA', 'Pendiente de Aprobacion'),
        ('A', 'Aprobado'),
        ('1', '1'), ('2', '2'),
        ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')), null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    forma_aprobacion = models.CharField(max_length=32, null=True, blank=True, verbose_name="Forma de aprobación",
     choices=(
        ('EqE', 'Equivalencia equivalente'),
        ('PC', 'Promocion en otra carrera'),
        ('P', 'Promocion'),
        ('Eq', 'Equivalencia'),
        ('ExE', 'Examen equivalente'),
        ('Ex', 'Examen')))
    acta_examen = models.CharField(max_length=32, null=True, blank=True)
    acta_promocion = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return u'%s, %s' % (self.materia, self.alumno)


class Inscripcion(models.Model):
    alumno = models.ForeignKey(
        Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    carrera = models.ForeignKey(
        Carrera, on_delete=models.CASCADE, related_name='inscripciones')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    comision = models.CharField(max_length=32, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        return u'%s-%s' % (self.alumno, self.materia)

class Graduado(models.Model):
    alumno = models.ForeignKey(
        AlumnoDeCarrera, on_delete=models.CASCADE, related_name='egresos'
    )
    fecha = models.DateField()

    def __str__(self):
        return u'%s-%s' % (self.alumno, self.fecha)

class Postulantes(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='postulantes')
    cantidad = models.IntegerField()
    fecha = models.DateField()

    class Meta:
        verbose_name_plural = "Postulantes"

    def __str__(self):
        return u'%s-%s-%s' % (self.fecha, self.carrera, self.cantidad)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carreras = models.ManyToManyField(Carrera)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil"

    def __str__(self):
        return u'%s' % self.user
