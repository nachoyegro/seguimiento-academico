from django import forms
from django.conf import settings
from django.core.management import call_command


class ImportadorForm(forms.Form):
    archivo = forms.FileField()
    command = ''
    userFeedback = ''

    def clean(self):
        if not self.errors:
            materias = self.cleaned_data['archivo']
            # Guardo el file
            path = settings.MEDIA_URL + materias.name
            self.save_file_in_media(materias, path)
            self.userFeedback = call_command(self.command, path)
            #messages.info(request,'Your export request is being processed')
        return self.cleaned_data

    def save_file_in_media(self, csv, path):
        with open(path, 'wb+') as destination:
            for chunk in csv.chunks():
                destination.write(chunk)


class ImportarMateriasCursadasForm(ImportadorForm):
    command = 'importar_materias_cursadas_guarani'


class ImportarDatosAlumnosForm(ImportadorForm):
    command = 'importar_alumnos'


class ImportarInscripcionesForm(ImportadorForm):
    command = 'importar_inscripciones'


class ImportarRequisitosForm(ImportadorForm):
    command = 'importar_requisitos'


class ImportarPlanesForm(ImportadorForm):
    command = 'importar_planes'
