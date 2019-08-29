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
    queryset = Alumno.objects.none()
    serializer_class = AlumnoSerializer

    def get_queryset(self):
        """
            - Chequeo las carreras que tiene asignada la persona
            - Devuelvo solo los alumnos que pertenecen a esa carrera
        """
        try:
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            alumnos = Alumno.objects.filter(pk__in=AlumnoDeCarrera.objects.filter(carrera__in=carreras).values_list('pk'))
        except:
            alumnos = Alumno.objects.none()
        return alumnos

class AlumnosDeCarreraView(generics.ListAPIView):
    queryset = Alumno.objects.none()
    serializer_class = AlumnoSerializer

    def get_queryset(self):
        """
        Retorna todos los alumnos de una determinada carrera,
        Si es que el usuario tiene permisos para ver esa carrera
        """
        alumnos = Alumno.objects.none()
        try:
            carrera = Carrera.objects.get(pk=self.kwargs['pk'])
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            if carrera in carreras:
                alumnos = Alumno.objects.filter(pk__in=AlumnoDeCarrera.objects.filter(carrera=carrera).values_list('pk'))
        except:
            pass
        return alumnos

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
