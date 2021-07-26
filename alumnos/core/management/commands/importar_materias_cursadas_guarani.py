from django.core.management.base import BaseCommand
import csv
from datetime import datetime, date
from core.materia_cursada_creator import MateriaCursadaCreator


class Command(BaseCommand):

    csvHeader = 'Legajo;DNI;Carrera;Regular;Calidad;Materia;Nombre;Fecha;Resultado;Nota;Forma Aprobación;Crédito;Acta_Promo;Acta_Ex;Plan'

    def add_arguments(self, parser):
        parser.add_argument('archivo')

    def handle(self, *args, **kwargs):
        path = kwargs['archivo']
        mc_creator = MateriaCursadaCreator()
        with open(path, 'r', encoding="utf8") as csvfile:
            csvReader = csv.reader(csvfile, delimiter=';')
            if not self.isValidCSVHeader(next(csvReader)):
                return 'CSV invalido, el encabezado debe ser: ' + self.csvHeader
            print('##### Importando materias cursadas ##### ', date.today())
            createdRecords = failedRows = 0
            failedIndeces = []
            exceptions = set()
            for csvRow in csvReader:
                try:
                    legajo = csvRow[0]
                    dni = csvRow[1]
                    cod_carrera = csvRow[2]
                    cod_materia = csvRow[5]
                    nombre_materia = csvRow[6]
                    fecha = datetime.strptime(csvRow[7], '%d/%m/%Y')
                    resultado = csvRow[8]
                    nota = csvRow[9]
                    forma_aprob = csvRow[10]
                    creditos = csvRow[11]
                    acta_promocion = csvRow[12]
                    acta_examen = csvRow[13]
                    plan = int(csvRow[14])
                    recordWasCreated = mc_creator.create(legajo=legajo, dni=dni, codigo_carrera=cod_carrera,
                                      codigo_materia=cod_materia, nombre_materia=nombre_materia,
                                      fecha=fecha, resultado=resultado, nota=nota,
                                      forma_aprobacion=forma_aprob, creditos=creditos,
                                      acta_promocion=acta_promocion, acta_examen=acta_examen,
                                      plan=plan)
                    if recordWasCreated:
                        createdRecords += 1
                except:
                    failedRows += 1
                    failedIndeces.append(i+2)
                    exceptions.add(str(e))

        userFeedback = 'Registros creados: ' + str(createdRecords)
        if failedRows > 0:
            userFeedback += '\nRegistros fallidos: ' + str(failedRows) + ', filas con errores: ' + str(failedIndeces)
            userFeedback += '\nExcepciones: ' + str(exceptions)
        return userFeedback

    def isValidCSVHeader(self, headerRow):
        return ';'.join(headerRow) == self.csvHeader
