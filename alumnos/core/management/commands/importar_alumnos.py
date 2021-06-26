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
            print('##### Importando alumnos ##### ', date.today())
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    try:
                        
                        legajo = row[0]
                        dni = row[1]
                        apellido = row[2]
                        nombre = row[3]
                        email = row[4]
                        fecha_str = row[5]
                        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
                        cod_carrera = row[6]
                        plan = row[7]
                        alumno, _ = Alumno.objects.get_or_create(legajo=legajo)
                        alumno.dni = dni
                        alumno.apellido = apellido
                        alumno.nombre = nombre
                        alumno.email = email
                        alumno.save()
                        """
                        dni = row[0]
                        apellido = row[1]
                        nombre = row[2]
                        email = row[3]
                        fecha_str = row[4]
                        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
                        cod_carrera = row[5]
                        plan = row[6]
                        alumno = Alumno.objects.get(dni=dni)
                        alumno.dni = dni
                        alumno.apellido = apellido
                        alumno.nombre = nombre
                        alumno.email = email
                        alumno.save()
                        """
                        carrera = Carrera.objects.get(codigo=cod_carrera)
                        plan_de_estudios = PlanDeEstudio.objects.get(
                            carrera=carrera, anio=int(plan))

                        alumno_de_carrera, _ = AlumnoDeCarrera.objects.get_or_create(
                            alumno=alumno, carrera=carrera)
                        alumno_de_carrera.plan = plan_de_estudios
                        alumno_de_carrera.fecha_inscripcion = fecha
                        alumno_de_carrera.save()
                    except Exception as e:
                        print(e)
                        print(row)
