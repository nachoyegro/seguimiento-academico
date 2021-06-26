from django.core.management.base import BaseCommand
from core.models import MateriaCursada
from core.serializers import MateriaCursadaSerializer
from pymemcache.client.base import PooledClient
from django.conf import settings
import json

cache = PooledClient(settings.MEMCACHED_URL, max_pool_size=4, encoding="utf-8")

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        carrera = kwargs['carrera']
        materias_cursadas = MateriaCursada.objects.filter(carrera__codigo=carrera)
        data = MateriaCursadaSerializer(materias_cursadas, many=True).data
        cache.set(carrera, json.dumps(data, ensure_ascii=False).encode('utf8'))
        print('La caché fue actualizada')


    def add_arguments(self , parser):
        parser.add_argument(
            '--carrera',
            help='Asigno una carrera para ser guardada por memcached',
        )
