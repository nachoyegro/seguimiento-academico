from django.core.management.base import BaseCommand
import csv
from core.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('materias.csv', 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            fila = 0
            for row in spamreader:
                carrera = Carrera.objects.get(codigo=row[0])
                plan = PlanDeEstudio.objects.get(nombre=row[1])
                materia, created = Materia.objects.get_or_create(siglas=row[4], codigo=row[2])
                materia.nombre = row[3]
                materia.save()
                materia_plan = MateriaEnPlan.objects.create(materia=materia, nombre=row[3])
                plan.materias.add(materia_plan)
                plan.save()
                fila += 1
