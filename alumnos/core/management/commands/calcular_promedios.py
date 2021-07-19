from django.core.management.base import BaseCommand
from core.models import MateriaCursada, AlumnoDeCarrera

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        carrera = kwargs['carrera']
        for alumno in AlumnoDeCarrera.objects.filter(carrera__codigo=carrera):
            suma = 0
            cantidad = 0
            promedio = None
            materias_cursadas = MateriaCursada.objects.filter(carrera__codigo=carrera, alumno=alumno.alumno)
            for cursada in materias_cursadas:
                try:
                    suma += float(cursada.nota)
                    cantidad += 1
                except Exception as e:
                    print(e)
            if cantidad:
                promedio = float(suma) / cantidad
            alumno.promedio = promedio
            alumno.save()
        

    def add_arguments(self , parser):
        parser.add_argument(
            '--carrera',
            help='Asigno una carrera para ser guardada por memcached',
        )
