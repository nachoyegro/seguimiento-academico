from django.core.management.base import BaseCommand
from core.models import MateriaCursada
from core.serializers import MateriaCursadaSerializer
from pymemcache.client.base import Client
from django.conf import settings

cache = Client(settings.MEMCACHED_URL, encoding="utf-8")

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        carrera = kwargs['carrera']
        materias_cursadas = MateriaCursada.objects.filter(carrera__codigo=carrera)
        data = MateriaCursadaSerializer(materias_cursadas, many=True).data
        cache.set(carrera, data)
        print('La caché fue actualizada')


    def add_arguments(self , parser):
        parser.add_argument(
            '--carrera',
            help='Asigno una carrera para ser guardada por memcached',
        )
