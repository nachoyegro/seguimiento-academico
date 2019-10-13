from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from core.models import Profile, Carrera

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        #Esto es solo para test. No va a estar en produccion
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        profile = Profile.objects.create(user=user)
        lids = Carrera.objects.get(codigo='W')
        profile.carreras.add(lids)
        profile.save()