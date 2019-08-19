from .models import *
from .serializers import *
from rest_framework import viewsets, renderers, generics
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.generic import View

class AlumnosView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class MateriasView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class ComisionView(viewsets.ModelViewSet):
    queryset = Comision.objects.all()
    serializer_class = ComisionSerializer

class CarrerasView(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

class AlumnosAPIV1(View):
    def get(self, *args, **kwargs):
        json = []
        for alumno in Alumno.objects.all():
            json_alumno = {"datos_personales": {},"cursadas": [], "carreras": []}
            json_alumno["datos_personales"]["nombre"] = alumno.nombre
            json_alumno["datos_personales"]["apellido"] = alumno.apellido
            json_alumno["datos_personales"]["dni"] = alumno.dni
            json_alumno["datos_personales"]["email"] = alumno.email
            json_alumno["legajo"] = alumno.legajo
            json_alumno["es_regular"] = alumno.es_regular
            for cursada in MateriaCursada.objects.filter(alumno=alumno):
                actual = {"materia": {}}
                actual["nota"] = cursada.nota
                actual["materia"]["nombre"] = cursada.materia.nombre
                actual["materia"]["siglas"] = cursada.materia.siglas
                actual["materia"]["codigo"] = MateriaEnPlan.objects.filter(materia=cursada.materia)[0].codigo
                json_alumno["cursadas"].append(actual)
            for carrera in AlumnoDeCarrera.objects.filter(alumno=alumno):
                carrera_json = {}
                carrera_json["nombre"] = carrera.carrera.nombre
                carrera_json["codigo"] = carrera.carrera.codigo
                json_alumno["carreras"].append(carrera_json)
            json.append(json_alumno)
        return JsonResponse(json, safe=False)
