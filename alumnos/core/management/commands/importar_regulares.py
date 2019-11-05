from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.utils.termcolors import make_style
from django.core import management
import csv
import datetime
from datetime import date, timedelta

class Command(BaseCommand):

    def handle(self, *args, **options):
        alumnos_file = args[0]
        alumnos =  csv.reader(alumnos_file, delimiter=';', quotechar='|')
        fila = 0
        for row in alumnos:
            if fila > 0:    
                apellido_nombre = row[0]
                #Row 1 es tipo dni
                dni = row[2]
                carrera_codigo = row[3]
                plan = row[4]
                legajo = row[5]
                promedio = row[6]
                coeficiente = row[7]
                posible_ci = row[8]
                try:
                    alumno = Alumno.objects.get(legajo=legajo)
                except:
                    alumno = None
                if alumno:
                    
            fila += 1