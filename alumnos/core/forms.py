from django import forms
from django.conf import settings
from django.core.management import call_command

class ImportarMateriasCursadasForm(forms.Form):
    materias_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ImportarMateriasCursadasForm, self).__init__(*args, **kwargs)
        self.command = 'importar_csv_guarani'

    def clean(self):
        if not self.errors:
            materias = self.cleaned_data['materias_file']
            #Guardo el file
            path = settings.MEDIA_URL + materias.name
            self.save_file_in_media(materias, path)
            call_command('importar_csv_guarani', path)
            #messages.info(request,'Your export request is being processed')
        return self.cleaned_data

    def save_file_in_media(self, csv, path):
        with open(path, 'wb+') as destination:
            for chunk in csv.chunks():
                destination.write(chunk)