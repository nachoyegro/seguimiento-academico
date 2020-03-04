from django.core.management.base import BaseCommand
import csv
from core.models import *


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # TPI
        tpi = Carrera.objects.create(nombre='TPI - Tecnicatura Universitaria en Programación Informática',
                                     codigo='P')

        # LDS
        lds = Carrera.objects.create(nombre='LDS - Licenciatura en Informática',
                                     codigo='W')

        PlanDeEstudio.objects.create(nombre='2015', carrera=tpi, anio=2015)
        PlanDeEstudio.objects.create(nombre='2015', carrera=lds, anio=2015)
        PlanDeEstudio.objects.create(nombre='2012', carrera=tpi, anio=2012)
        PlanDeEstudio.objects.create(nombre='2012', carrera=lds, anio=2012)
        PlanDeEstudio.objects.create(nombre='2010', carrera=tpi, anio=2010)
        PlanDeEstudio.objects.create(nombre='2010', carrera=lds, anio=2010)
