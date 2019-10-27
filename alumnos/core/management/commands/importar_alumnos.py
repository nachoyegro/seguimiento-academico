from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from core.models import Alumno


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
                    apellido = row[1]
                    nombre = row[2]
                    dni = row[3]
                    email = row[4]
                    try:
                        alumno = Alumno.objects.get(legajo=legajo)
                        alumno.apellido = apellido
                        alumno.nombre = nombre
                        alumno.dni = dni
                        alumno.email = email
                        alumno.save()
                    except:
                        pass
