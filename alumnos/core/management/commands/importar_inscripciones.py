from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.models import Alumno, Materia, Carrera, Inscripcion, AlumnoDeCarrera


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
                        dni = row[1]
                        legajo = row[2]
                        cod_materia = row[3]
                        comision = row[4]
                        fecha_str = row[5].split(' ')[0]
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
                            plan = PlanDeEstudio.objects.filter(carrera=carrera).order_by('-anio')[0]
                            alumno_de_carrera.plan = plan
                            alumno_de_carrera.save()

                        materia = Materia.objects.get(
                            codigo=cod_materia.zfill(5))

                        Inscripcion.objects.create(
                            alumno=alumno, materia=materia, carrera=carrera, fecha=fecha, comision=comision)
                    except:
                        print(row)
