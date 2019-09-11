from django.core.management.base import BaseCommand
import csv
from core.models import Carrera, Alumno, Materia, MateriaCursada, PlanDeEstudio, AlumnoDeCarrera, MateriaEnPlan
from datetime import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        carrera_iaci, created = Carrera.objects.get_or_create(codigo='D')
        with open(path, 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    legajo = row[0]
                    cod_materia = row[1]
                    nombre_materia = row[2]
                    fecha = datetime.strptime(row[3], '%d/%m/%Y')
                    result = row[4]
                    nota = row[5]
                    forma_aprob = row[6]
                    creditos = row[7]
                    acta_promocion = row[8]
                    acta_examen = row[9]
                    plan = row[10]
                    alumno, created = Alumno.objects.get_or_create(legajo=legajo)
                    alumno_carrera, created = AlumnoDeCarrera.objects.get_or_create(alumno=alumno, carrera=carrera_iaci)
                    materia, created = Materia.objects.get_or_create(codigo=cod_materia)
                    if created:
                        materia.nombre = nombre_materia
                        materia.save()
                    materia_cursada = MateriaCursada.objects.create(alumno=alumno, carrera=carrera_iaci, 
                                        materia=materia, fecha=fecha, resultado=result, nota=nota)
                    plan_de_estudio, created = PlanDeEstudio.objects.get_or_create(nombre=plan, carrera=carrera_iaci)
                    if created:
                        plan_de_estudio.anio = plan
                        plan_de_estudio.save()
                
                    materia_en_plan, created = MateriaEnPlan.objects.get_or_create(materia=materia, plan=plan_de_estudio)
                    if created:
                        materia_en_plan.creditos = creditos
                        materia_en_plan.codigo = cod_materia
                        materia_en_plan.save()
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