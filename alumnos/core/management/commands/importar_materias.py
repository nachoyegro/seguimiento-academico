from django.core.management.base import BaseCommand
import csv
from core.models import Carrera, PlanDeEstudio, Materia, MateriaEnPlan

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('materias.csv', 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            fila = 0
            for row in spamreader:
                carrera = Carrera.objects.get(codigo=row[0])
                plan = PlanDeEstudio.objects.get(nombre=row[1], carrera=carrera)
                codigo = row[2].zfill(5) #Lo relleno con ceros hasta llegar a 5
                materia, _ = Materia.objects.get_or_create(siglas=row[4])
                materia.nombre = row[3]
                materia.save()
                MateriaEnPlan.objects.create(materia=materia, nombre=row[3], codigo=codigo, plan=plan)
                fila += 1
