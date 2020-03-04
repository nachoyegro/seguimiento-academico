from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from core.models import MateriaEnPlan
import random


class Command(BaseCommand):

    nucleos = ['A', 'B', 'C']
    areas = ['Area 1', 'Area 2', 'Area 3']

    def handle(self, *args, **kwargs):
        result = []
        for materia in MateriaEnPlan.objects.filter(plan__carrera__codigo='D'):
            result.append({'id': materia.id,
                           'plan': '2003',
                           'area': self.areas[random.randint(0, 2)],
                           'nucleo': self.nucleos[random.randint(0, 2)],
                           'codigo': materia.materia.codigo,
                           'creditos': materia.creditos,
                           'obligatorias': [],
                           'recomendadas': [],
                           'cantidad_obligatorias_de': random.randint(0, 50),
                           'materia': materia.materia.nombre})
        print(result)
