from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.materia_cursada_creator import MateriaCursadaCreator


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        mc_creator = MateriaCursadaCreator()
        with open(path, 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            print('##### Importando materias cursadas ##### ', date.today())
            for fila, row in enumerate(spamreader):
                if fila > 0:
                    try:
                        legajo = row[0]
                        dni = row[1]
                        cod_carrera = row[2]
                        cod_materia = row[5]
                        nombre_materia = row[6]
                        fecha = datetime.strptime(row[7], '%d/%m/%Y')
                        resultado = row[8]
                        nota = row[9]
                        forma_aprob = row[10]
                        creditos = row[11]
                        acta_promocion = row[12]
                        acta_examen = row[13]
                        plan = int(row[14])
                        mc_creator.create(legajo=legajo, dni=dni, codigo_carrera=cod_carrera,
                                          codigo_materia=cod_materia, nombre_materia=nombre_materia,
                                          fecha=fecha, resultado=resultado, nota=nota,
                                          forma_aprobacion=forma_aprob, creditos=creditos,
                                          acta_promocion=acta_promocion, acta_examen=acta_examen,
                                          plan=plan)
                    except:
                        print(row)
