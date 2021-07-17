from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from core.models import Carrera, PlanDeEstudio, Materia, MateriaEnPlan, Area


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            createdPlans = createdSubjects = createdPlanSubjects = failedRows = 0
            nonExistentCareers = set()
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    cod_carrera = row[0]
                    anio_plan = row[1]
                    cuatrimestre = row[2]
                    nombre_nucleo = row[3]
                    nombre_area = row[4]
                    cod_materia = row[5].zfill(5)
                    creditos = row[6]
                    nombre_materia = row[7]

                    try:
                        carrera = Carrera.objects.get(codigo=cod_carrera)
                    except Carrera.DoesNotExist:
                        failedRows += 1
                        nonExistentCareers.add(cod_carrera)
                        continue

                    plan, created = PlanDeEstudio.objects.get_or_create(
                        anio=anio_plan, carrera=carrera)
                    if created:
                        plan.nombre = anio_plan
                        plan.save()
                        createdPlans += 1

                    materia, created = Materia.objects.get_or_create(
                        codigo=cod_materia)
                    if created:
                        materia.nombre = nombre_materia
                        materia.save()
                        createdSubjects += 1

                    area, created = Area.objects.get_or_create(
                        nombre=nombre_area, carrera=carrera)

                    materia_en_plan, created = MateriaEnPlan.objects.get_or_create(
                        materia=materia, plan=plan)
                    if created:
                        materia_en_plan.orden_cuatrimestral = int(
                            cuatrimestre) if cuatrimestre else None
                        materia_en_plan.area = area
                        materia_en_plan.nucleo = nombre_nucleo
                        materia_en_plan.codigo = cod_materia
                        materia_en_plan.creditos = creditos
                        materia_en_plan.save()
                        createdPlanSubjects += 1

        userFeedback = 'Registros creados: Planes: ' + str(createdPlans) + ', Materias: ' + str(createdSubjects) + ', Materias asignadas a planes: ' + str(createdPlanSubjects)
        if failedRows > 0:
            userFeedback += ', Registros no creados: ' + str(failedRows) + ', carreras inexistentes: ' + str(nonExistentCareers)
        return userFeedback
