from core.models import Carrera, Alumno, Materia, MateriaCursada, PlanDeEstudio, AlumnoDeCarrera, MateriaEnPlan
from datetime import datetime


class MateriaCursadaCreator:

    def create(self, **kwargs):
        legajo = kwargs['legajo']
        dni = kwargs['dni']
        cod_carrera = kwargs['codigo_carrera']
        cod_materia = kwargs['codigo_materia']
        nombre_materia = kwargs['nombre_materia']
        fecha = kwargs['fecha']
        resultado = kwargs['resultado']
        nota = kwargs['nota']
        # Si no tiene nota, y el resultado es 'A', entonces la nota tiene que ser 'A'
        if not nota and resultado == 'A':
            nota = 'A'
        forma_aprob = kwargs['forma_aprobacion']
        creditos_arg = kwargs['creditos']
        creditos = int(creditos_arg) if creditos_arg else None
        acta_promocion = kwargs['acta_promocion']
        acta_examen = kwargs['acta_examen']
        plan = kwargs['plan']

        carrera = Carrera.objects.get(codigo=cod_carrera)
        alumno, created = Alumno.objects.get_or_create(legajo=legajo)
        if dni:
            alumno.dni = dni
            alumno.save()
        alumno_carrera, alumno_carrera_created = AlumnoDeCarrera.objects.get_or_create(
            alumno=alumno, carrera=carrera)
        materia, created = Materia.objects.get_or_create(codigo=cod_materia)
        # Si la materia fue creada, le pongo nombre
        if created:
            materia.nombre = nombre_materia
            materia.save()
        plan_de_estudio, created = PlanDeEstudio.objects.get_or_create(
            anio=plan, carrera=carrera)
        # Si fue creado nuevo, le pongo nombre al plan
        if created:
            plan_de_estudio.nombre = plan
            plan_de_estudio.save()
        # Actualizo el plan de estudios actual del alumno en esa carrera
        if not alumno_carrera.plan or plan_de_estudio > alumno_carrera.plan:
            alumno_carrera.plan = plan_de_estudio
            alumno_carrera.save()
        materia_en_plan, created = MateriaEnPlan.objects.get_or_create(
            materia=materia, plan=plan_de_estudio)
        if created:
            materia_en_plan.nombre_en_plan = nombre_materia
            materia_en_plan.codigo = cod_materia
        materia_en_plan.creditos = creditos
        materia_en_plan.save()
        materia_cursada = MateriaCursada.objects.create(
            alumno=alumno, materia=materia_en_plan, carrera=carrera, fecha=fecha, resultado=resultado, forma_aprobacion=forma_aprob, nota=nota)


"""
Resultados
U: Libre
U: Ausente
R: Reprobó
A: Regular
P: Acreditó
N: No Acreditó
E: Pendiente Aprobación
E: Pendiente Virtual
"""
