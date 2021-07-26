from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from core.models import Carrera, PlanDeEstudio, Materia, MateriaEnPlan, Area


class Command(BaseCommand):

    csvHeader = 'Codigo Carrera;Plan;Cuatrimestre;Nucleo;Area;Codigo;Creditos;Nombre'

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            if not self.isValidCSVHeader(next(csvReader)):
                return 'CSV invalido, el encabezado debe ser: ' + self.csvHeader
            createdPlans = createdSubjects = createdPlanSubjects = failedRows = 0
            failedIndeces = []
            exceptions = set()
            for i, csvRow in enumerate(csvReader):
                try:
                    cod_carrera = csvRow[0]
                    anio_plan = csvRow[1]
                    cuatrimestre = csvRow[2]
                    nombre_nucleo = csvRow[3]
                    nombre_area = csvRow[4]
                    cod_materia = csvRow[5].zfill(5)
                    creditos = csvRow[6]
                    nombre_materia = csvRow[7]

                    carrera = Carrera.objects.get(codigo=cod_carrera)

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
                except Exception as e:
                    failedRows += 1
                    failedIndeces.append(i+2)
                    exceptions.add(str(e))

        userFeedback = 'Registros creados: Planes: ' + str(createdPlans) + ', Materias: ' + str(createdSubjects) + ', Materias asignadas a planes: ' + str(createdPlanSubjects)
        if failedRows > 0:
            userFeedback += '\nRegistros fallidos: ' + str(failedRows) + ', filas con errores: ' + str(failedIndeces)
            userFeedback += '\nExcepciones: ' + str(exceptions)
        return userFeedback

    def isValidCSVHeader(self, headerRow):
        return ';'.join(headerRow) == self.csvHeader