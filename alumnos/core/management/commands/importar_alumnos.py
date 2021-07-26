from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.models import *


class Command(BaseCommand):

    csvHeader = 'Legajo;DNI;Apellido;Nombre;Email;Fecha;Carrera;Plan'

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        with open(path, 'r', encoding="utf8") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            if not self.isValidCSVHeader(next(csvReader)):
                return '(ToDo: validar con CSV ej) CSV invalido, el encabezado debe ser: ' + self.csvHeader
            print('##### Importando alumnos ##### ', date.today())
            createdRecords = updatedRecords = failedRows = 0
            failedIndeces = []
            exceptions = set()
            for csvRow in csvReader:
                try:                    
                    legajo = csvRow[0]
                    dni = csvRow[1]
                    apellido = csvRow[2]
                    nombre = csvRow[3]
                    email = csvRow[4]
                    fecha_str = csvRow[5]
                    fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
                    cod_carrera = csvRow[6]
                    plan = csvRow[7]
                    alumno, createdStudent = Alumno.objects.get_or_create(legajo=legajo)
                    alumno.dni = dni
                    alumno.apellido = apellido
                    alumno.nombre = nombre
                    alumno.email = email
                    alumno.save()

                    carrera = Carrera.objects.get(codigo=cod_carrera)
                    plan_de_estudios = PlanDeEstudio.objects.get(
                        carrera=carrera, anio=int(plan))

                    alumno_de_carrera, createdCareerStudent = AlumnoDeCarrera.objects.get_or_create(
                        alumno=alumno, carrera=carrera)
                    alumno_de_carrera.plan = plan_de_estudios
                    alumno_de_carrera.fecha_inscripcion = fecha
                    alumno_de_carrera.save()
                    if createdStudent or createdCareerStudent:
                        createdRecords += 1
                    else:
                        updatedRecords += 1
                except Exception as e:
                    failedRows += 1
                    failedIndeces.append(i+2)
                    exceptions.add(str(e))

        userFeedback = 'Registros creados: ' + str(createdRecords) + ', Registros actualizados: ' + str(updatedRecords)
        if failedRows > 0:
            userFeedback += '\nRegistros fallidos: ' + str(failedRows) + ', filas con errores: ' + str(failedIndeces)
            userFeedback += '\nExcepciones: ' + str(exceptions)
        return userFeedback

    def isValidCSVHeader(self, headerRow):
        return ';'.join(headerRow) == self.csvHeader
