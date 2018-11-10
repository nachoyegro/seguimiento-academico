from django.core.management.base import BaseCommand
import csv
from core.models import *

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        #TPI
        tpi = Carrera.objects.create(nombre='TPI - Tecnicatura Universitaria en Programación Informática',
                                     codigo='P')
        plan_2010 = PlanDeEstudio.objects.create(nombre='2010')
        tpi.planes.add(plan_2010)
        tpi.save()


        #LDS
        lds = Carrera.objects.create(nombre='LDS - Licenciatura en Informática',
        codigo='W')
        plan_2012 = PlanDeEstudio.objects.create(nombre='2012')
        lds.planes.add(plan_2012)
        lds.save()
