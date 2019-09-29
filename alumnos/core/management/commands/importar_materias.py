from django.core.management.base import BaseCommand
import csv
from core.models import Carrera, PlanDeEstudio, Materia, MateriaEnPlan

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    carrera, carrera_creada = Carrera.objects.get_or_create(codigo=row[0])
                    plan, plan_creado = PlanDeEstudio.objects.get_or_create(anio=row[1], carrera=carrera)
                    cuatrimestre = int(row[2])
                    nucleo = row[3] ## TODO: validador de nucleos
                    area, created = Area.objects.get_or_create(nombre=row[4]) ##TODO: codigos de areas
                    codigo = row[5].zfill(5) #Lo relleno con ceros hasta llegar a 5
                    nombre_materia = row[6]

                    materia, materia_creada = Materia.objects.get_or_create(codigo=codigo)
                    if materia_creada:
                        materia.nombre = nombre_materia
                        materia.save()
                    materia_en_plan, creada = MateriaEnPlan.objects.get_or_create(materia=materia, plan=plan)
                    materia_en_plan.nombre = nombre_materia
                    materia_en_plan.codigo = codigo
                    materia_en_plan.area = area
                    materia_en_plan.nucleo = nucleo
                    materia_en_plan.orden_cuatrimestral = cuatrimestre
                    materia_en_plan.save()

                    fila += 1
