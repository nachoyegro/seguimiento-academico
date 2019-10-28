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
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    cod_carrera = row[0]
                    anio_plan = row[1]
                    cuatrimestre = row[2]
                    nombre_nucleo = row[3]
                    nombre_area = row[4]
                    cod_materia = row[5].zfill(5)
                    nombre_materia = row[6]

                    carrera = Carrera.objects.get(codigo=cod_carrera)
                    plan, created = PlanDeEstudio.objects.get_or_create(
                        anio=anio_plan, carrera=carrera)
                    if created:
                        plan.nombre = anio_plan
                        plan.save()

                    materia, created = Materia.objects.get_or_create(
                        codigo=cod_materia)
                    if created:
                        materia.nombre = nombre_materia
                        materia.save()

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
                        materia_en_plan.save()
