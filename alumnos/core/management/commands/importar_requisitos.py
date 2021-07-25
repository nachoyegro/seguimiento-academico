from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.models import *


class Command(BaseCommand):

    csvHeader = 'Carrera;Plan;Materia;Obligatorias;Recomendadas'

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            if not self.isValidCSVHeader(next(csvReader)):
                return 'CSV invalido, el encabezado debe ser: ' + self.csvHeader
            print('##### Importando inscripciones ##### ', date.today())
            for csvRow in csvReader:
                try:
                    cod_carrera = csvRow[0]
                    plan_anio = csvRow[1]
                    cod_materia = csvRow[2].zfill(5)
                    obligatorias = csvRow[3]
                    recomendadas = csvRow[4]
                    carrera = Carrera.objects.get(codigo=cod_carrera)
                    plan = PlanDeEstudio.objects.get(
                        anio=int(plan_anio), carrera=carrera)
                    materia = MateriaEnPlan.objects.get(
                        plan=plan, materia__codigo=cod_materia)
                    # Obligatorias
                    for obligatoria in obligatorias.split(','):
                        if obligatoria:
                            materia_obligatoria = MateriaEnPlan.objects.get(
                                materia__codigo=obligatoria.replace(' ', '').replace('\n', '').zfill(5), plan=plan)
                            materia.obligatorias.add(materia_obligatoria)
                    # Recomendadas
                    for recomendada in recomendadas.split(','):
                        if recomendada:
                            materia_recomendada = MateriaEnPlan.objects.get(
                                materia__codigo=recomendada.replace(' ', '').replace('\n', '').zfill(5), plan=plan)
                            materia.recomendadas.add(materia_recomendada)
                    materia.save()
                except:
                    print(csvRow)

    def isValidCSVHeader(self, headerRow):
        return ';'.join(headerRow) == self.csvHeader
