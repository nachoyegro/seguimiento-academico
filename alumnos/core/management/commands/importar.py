from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print('Importando')
        call_command('inicial')
        print('Importando materias')
        call_command('importar_materias')
        print('Importando alumnos')
        call_command('importar_alumnos')
