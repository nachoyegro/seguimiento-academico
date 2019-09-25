from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        #print('Importando')
        #call_command('inicial')
        #print('Importando materias')
        #call_command('importar_materias')
        #print('Importando alumnos')
        #call_command('importar_alumnos')
        call_command('importar_csv_guarani', os.path.join(settings.DOCS_URL, 'alumnos_guarani.csv'))
