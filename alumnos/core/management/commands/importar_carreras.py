from django.core.management.base import BaseCommand
import csv
from core.models import Carrera, PlanDeEstudio, Materia, MateriaEnPlan
from datetime import datetime

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('docs/carreras.csv', 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    Carrera.objects.create(codigo=row[0], nombre=row[1], fecha_creacion=datetime.strptime(row[2], "%d/%m/%Y").date())
