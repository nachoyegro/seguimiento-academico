from django.core.management.base import BaseCommand
import csv
from core.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        carrera_tpi = Carrera.objects.get(codigo='P')
        carrera_lds = Carrera.objects.get(codigo='W')
        with open('alumnos-reales.csv', 'r', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            fila = 0
            sin_alumnos = 0
            for row in spamreader:
                if fila >= 15:
                    tpi = carrera_tpi if 'P' in row[2] else False
                    lds = carrera_lds if 'W' in row[3] else False #Hay campos como W!
                    sexo = row[4]
                    numero_inscripto = row[5]
                    dni = row[6]
                    legajo = row[7]
                    nombre = row[8]
                    apellido = row[9]
                    if nombre and apellido:
                        ci = row[10]
                        plan = row[11]
                        telefono = row[40]
                        celular = row[41]
                        mail = row[42]
                        compartible = row[43] #Esto lo puedo hacer con una funcion
                        rpd = row[44] #?
                        situacion = row[45]
                        status = row[47]
                        condicion = row[48] #Asked, No aparecio, TPI, casiTPI, casiTPI problemas, casiTPI?, finTPI, avanzadoTPI, Ingresante, simultaneidad, ingreso directo, 2x1, 2x1old
                        regularidad = row[49]
                        tiene_beca = row[50]
                        tiene_tutor = row[51]
                        tiene_pc = row[52]
                        tiene_pendrive = row[53]
                        tiene_portatil = row[54]
                        comentario = row[55]
                        #57 ... 61 TutCyT	cpi-doc	cpi-est	cpi-grad -> listas
                        observacion = row[62]
                        Tfinal = row[105]
                        Director = row[106]
                        resolucion = row[107]
                        aceptacion = row[108]
                        finalizacion = row[109]
                        tema = row[110]
                        _  = row[111]
                        mate1_c1 = row[112]
                        mate1_c2 = row[113]
                        mate1_c3 = row[114]
                        mate2_c1 = row[115]
                        mate2_c2 = row[116]
                        obj1_c1 = row[117]
                        obj1_c2 = row[118]
                        _ = row[119]
                        _ = row[120]
                        observacion = row[121]
                        _  = row[122]
                        #Si no hay nombre ni apellido entonces es una linea en blanco
                        persona = Persona.objects.create(nombre=nombre, apellido=apellido, dni=dni, email=mail)
                        alumno = Alumno.objects.create(datos_personales=persona, legajo=legajo,
                                sexo=sexo, cuatrimestre_inscripto=ci, telefono=telefono, celular=celular,
                                comentario=comentario, observacion=observacion)
                        if tpi: alumno.carreras.add(tpi)
                        if lds: alumno.carreras.add(lds)
                        alumno.save()
                        sin_alumnos = 0
                        materias = {'len': 63, #equivalencia?
                                    'mat': 64, #equivalencia?
                                    'epl': 65, #equivalencia?
                                    'sem_ts': 104, #
                                    'sem_str': 95,#----
                                    'syd': 89, #
                                    'ing1': 66, #
                                    'ing2': 67, #
                                    'mat1': 68, #
                                    'mat2': 75, #
                                    'mat3': 125, #
                                    'inpr': 69, #
                                    'orga': 70, #
                                    'bd': 71, #
                                    'ed': 72, #
                                    'obj1': 73, #
                                    'obj2': 74, #
                                    'obj3': 87, #
                                    'red': 76, #
                                    'so': 77, #
                                    'labo': 78,
                                    'pf': 79, #
                                    'uis': 80, #
                                    'epers': 81, #
                                    'iisoft': 82, #
                                    'pconc': 83, #
                                    'dapp': 84, #
                                    'seg': 85, #
                                    'lfa': 86, #
                                    'clp': 88, #
                                    'games': 90, #
                                    'deraut': 91, #
                                    'proysl': 92, #
                                    'sem_micro': 93, #
                                    'sem_tvd': 94, #
                                    'sem_web': 96, #
                                    'tti': 102, #
                                    'ttu': 103, #
                                    'am1'	: 123, #
                                    'proba': 124, #
                                    'gproy': 126, #
                                    'ingreq': 127,
                                    'pdes': 128, #
                                    'lyp': 129, #
                                    'algo': 130, #
                                    'arq1': 131, #
                                    'arq2': 132, #
                                    'tco': 133, #
                                    'arqco': 134, #
                                    'parse': 135, #
                                    'legal': 136 #
                                    }
                        for sigla, indice in materias.items():
                            materia, created = Materia.objects.get_or_create(siglas=sigla)
                            if created:
                                print(sigla)
                            nota = row[indice]
                            if nota and 'c' not in nota and 'C' not in nota:
                                cursada = MateriaCursada.objects.create(materia=materia,
                                alumno=alumno, nota=nota)
                    else:
                        sin_alumnos += 1
                    #Si acumulo 3 lineas sin alumnos termino
                    if sin_alumnos >= 3:
                        break
                fila += 1
