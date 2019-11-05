from .models import *
from .serializers import *
from .forms import ImportarMateriasCursadasForm, ImportarDatosAlumnosForm, ImportarInscripcionesForm
from rest_framework import viewsets, renderers, generics
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


class MateriasCursadasView(viewsets.ModelViewSet):
    queryset = MateriaCursada.objects.none()
    serializer_class = MateriaCursadaSerializer

    def get_queryset(self):
        """
            - Chequeo las carreras que tiene asignada la persona
            - Devuelvo solo las materias cursadas que pertenecen a esa carrera
        """
        try:
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            alumnos = MateriaCursada.objects.filter(carrera__in=carreras)
        except:
            alumnos = MateriaCursada.objects.none()
        return alumnos


class InscripcionesView(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.none()
    serializer_class = InscripcionSerializer

    def get_queryset(self):
        """
            - Chequeo las carreras que tiene asignada la persona
            - Devuelvo solo las inscripciones que pertenecen a esa carrera
        """
        try:
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            alumnos = Inscripcion.objects.filter(carrera__in=carreras)
        except:
            alumnos = Inscripcion.objects.none()
        return alumnos


class MateriasEnPlanView(generics.ListAPIView):
    queryset = MateriaEnPlan.objects.none()
    serializer_class = MateriaEnPlanSerializer

    def get_queryset(self):
        """
        Retorna todas las materias pertenecientes al plan que busco,
        si el usuario tiene permisos para ver esa carrera
        """
        materias = MateriaEnPlan.objects.none()
        try:
            carrera = Carrera.objects.get(codigo=self.kwargs['codigo_carrera'])
            plan = PlanDeEstudio.objects.get(
                anio=self.kwargs['plan_anio'], carrera=carrera)
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            if carrera in carreras:
                materias = MateriaEnPlan.objects.filter(plan=plan)
        except:
            pass
        return materias


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
            alumnos = Alumno.objects.filter(pk__in=AlumnoDeCarrera.objects.filter(
                carrera__in=carreras).values_list('pk'))
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
            carrera = Carrera.objects.get(codigo=self.kwargs['codigo_carrera'])
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            if carrera in carreras:
                alumnos = Alumno.objects.filter(
                    pk__in=AlumnoDeCarrera.objects.filter(carrera=carrera).values_list('pk'))
        except:
            pass
        return alumnos


class MateriasView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer


class CarrerasView(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

    def get_queryset(self):
        """
        Retorna todas las carreras que puede ver el usuario actual
        """
        carreras = Carrera.objects.none()
        try:
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
        except:
            pass
        return carreras


class ImportadorView(View):
    form = None
    template = ''

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, **kwargs):
        form = self.form()
        return render(request, self.template, dict(form=form))

    def post(self, request):
        response = dict()
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            response['form'] = form
        return render(request, self.template, response)


class ImportarMateriasCursadasView(ImportadorView):
    form = ImportarMateriasCursadasForm
    template = 'importadores/importador_materias_cursadas.html'


class ImportarDatosAlumnosView(ImportadorView):
    form = ImportarDatosAlumnosForm
    template = 'importadores/importador_datos_alumnos.html'


class ImportarInscripcionesView(ImportadorView):
    form = ImportarInscripcionesForm
    template = 'importadores/importador_inscripciones.html'
