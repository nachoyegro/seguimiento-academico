from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from core.forms import ImportarMateriasCursadasForm
from core.models import Carrera, Alumno
from django.conf import settings


class ImportarMateriasCursadasFormTest(TestCase):

    def setUp(self):
        # Creo la carrera de IACI
        Carrera.objects.create(codigo='D')
        self.path = '/code/alumnos/docs/alumnos_guarani.csv'
        with open(self.path, 'rb') as infile:
            self.data = {
                'archivo': SimpleUploadedFile(self.path, infile.read())
            }

    def test_sin_archivo(self):
        form = ImportarMateriasCursadasForm()
        self.assertTrue(not form.is_valid())

    def test_con_archivo(self):
        # El primer argumento es request.POST, el segundo es request.FILES
        form = ImportarMateriasCursadasForm({}, self.data)
        self.assertTrue(form.is_valid())

    def test_alumnos_creados(self):
        form = ImportarMateriasCursadasForm({}, self.data)
        # Corro el clean del form para que importe el archivo
        form.is_valid()
        # El csv tiene 3 alumnos
        self.assertEquals(Alumno.objects.all().count(), 3)
