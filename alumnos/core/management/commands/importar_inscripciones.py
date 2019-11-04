from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from core.models import Alumno, Materia, Carrera, Inscripcion


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
                    legajo = row[1]
                    cod_materia = row[2]
                    comision = row[3]
                    fecha_str = row[4].split(' ')[0]
                    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

                    carrera = Carrera.objects.get(codigo=cod_carrera)
                    alumno = Alumno.objects.get(legajo=legajo)
                    materia = Materia.objects.get(
                        codigo=cod_materia.zfill(5))

                    Inscripcion.objects.create(
                        alumno=alumno, materia=materia, carrera=carrera, fecha=fecha, comision=comision)
