from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.models import *


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print('##### Importando inscripciones ##### ', date.today())
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    try:
                        cod_carrera = row[0]
                        plan_anio = row[1]
                        cod_materia = row[2].zfill(5)
                        obligatorias = row[3]
                        recomendadas = row[4]
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
                        print(row)
                fila += 1
