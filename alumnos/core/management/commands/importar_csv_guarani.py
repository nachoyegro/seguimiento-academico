from django.core.management.base import BaseCommand
import csv
from core.models import Carrera, Alumno, Materia, MateriaCursada, PlanDeEstudio, AlumnoDeCarrera, MateriaEnPlan
from datetime import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    legajo = row[0]
                    #dni = row[1]
                    cod_carrera = row[2]
                    cod_materia = row[5]
                    nombre_materia = row[6]
                    fecha = datetime.strptime(row[7], '%d/%m/%Y')
                    resultado = row[8]
                    nota = row[9]
                    if not nota and resultado == 'A':
                        nota = 'A'
                    forma_aprob = row[10]
                    creditos = int(row[11]) if row[11] else None
                    acta_promocion = row[12]
                    acta_examen = row[13]
                    plan = row[14]
                    carrera = Carrera.objects.get(codigo=cod_carrera)
                    alumno, created = Alumno.objects.get_or_create(legajo=legajo)
                    alumno_carrera, created = AlumnoDeCarrera.objects.get_or_create(alumno=alumno, carrera=carrera)
                    materia, created = Materia.objects.get_or_create(codigo=cod_materia)
                    if created:
                        materia.nombre = nombre_materia
                        materia.save()
                    plan_de_estudio, created = PlanDeEstudio.objects.get_or_create(anio=plan, carrera=carrera)
                    if created:
                        plan_de_estudio.nombre = plan
                        plan_de_estudio.save()
                
                    materia_en_plan, created = MateriaEnPlan.objects.get_or_create(materia=materia, plan=plan_de_estudio)
                    if created:
                        materia_en_plan.creditos = creditos
                        materia_en_plan.codigo = cod_materia
                        materia_en_plan.save()
	
                    materia_cursada = MateriaCursada.objects.create(alumno=alumno, materia=materia_en_plan,carrera=carrera, fecha=fecha, resultado=resultado, forma_aprobacion=forma_aprob, nota=nota or None)
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
