from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print('Importando Carreras')
        call_command('importar_carreras')
        print('Importando Cursadas de IACI')
        call_command('importar_csv_guarani', os.path.join(
            settings.DOCS_URL, 'alumnos_guarani.csv'))
        print('Creando SuperUser')
        call_command('create_superuser')
        print('Importando Planes')
        call_command('importar_planes', os.path.join(
            settings.BASE_DIR, 'data/planes_lds.csv'))
        print('Importando Requisitos')
        call_command('importar_requisitos', os.path.join(
            settings.BASE_DIR, 'data/requisitos_lds.csv'))
        print('Importando Materias Cursadas')
        call_command('importar_materias_cursadas_guarani', os.path.join(
            settings.BASE_DIR, 'data/lds2021.csv'))
