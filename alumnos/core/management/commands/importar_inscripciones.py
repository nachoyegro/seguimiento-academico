from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.models import PlanDeEstudio, Alumno, Materia, Carrera, Inscripcion, AlumnoDeCarrera


class Command(BaseCommand):

    csvHeader = 'Carrera;DNI;Legajo;Materia;Comision;Fecha'

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            if not self.isValidCSVHeader(next(csvReader)):
                return '(ToDo: validar con CSV ej) CSV invalido, el encabezado debe ser: ' + self.csvHeader
            print('##### Importando inscripciones ##### ', date.today())
            for csvRow in csvReader:
                try:
                    cod_carrera = csvRow[0]
                    dni = csvRow[1]
                    legajo = csvRow[2]
                    cod_materia = csvRow[3]
                    comision = csvRow[4]
                    fecha_str = csvRow[5].split(' ')[0]
                    fecha = datetime.strptime(fecha_str, '%d/%m/%Y')

                    carrera = Carrera.objects.get(codigo=cod_carrera)
                    alumno, _ = Alumno.objects.get_or_create(
                        legajo=legajo)
                    if dni:
                        alumno.dni = dni
                        alumno.save()
                    alumno_de_carrera, _ = AlumnoDeCarrera.objects.get_or_create(
                        alumno=alumno, carrera=carrera)
                    if not alumno_de_carrera.plan:
                        # Si no tiene plan
                        # Entonces, le pongo el plan actual
                        plan = PlanDeEstudio.objects.filter(
                            carrera=carrera).order_by('-anio')[0]
                        alumno_de_carrera.plan = plan
                        alumno_de_carrera.save()

                    materia = Materia.objects.get(
                        codigo=cod_materia.zfill(5))

                    Inscripcion.objects.get_or_create(
                        alumno=alumno, materia=materia, carrera=carrera, fecha=fecha, comision=comision)
                except Exception as e:
                    print(e)

    def isValidCSVHeader(self, headerRow):
        # ToDo: No tengo CSV de ejemplo. validar.
        return ';'.join(headerRow) == self.csvHeader
