from .models import *
from .serializers import *
from .forms import *
from rest_framework import viewsets, renderers, generics
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


class AlumnosAPIV1(View):
    def get(self, *args, **kwargs):
        json = []
        for alumno in Alumno.objects.all():
            json_alumno = {"datos_personales": {},
                           "cursadas": [], "carreras": []}
            json_alumno["datos_personales"]["nombre"] = alumno.nombre
            json_alumno["datos_personales"]["apellido"] = alumno.apellido
            json_alumno["datos_personales"]["dni"] = alumno.dni
            json_alumno["datos_personales"]["email"] = alumno.email
            json_alumno["legajo"] = alumno.legajo
            json_alumno["es_regular"] = alumno.es_regular
            for cursada in MateriaCursada.objects.filter(alumno=alumno):
                actual = {"materia": {}}
                actual["nota"] = cursada.nota
                actual["materia"]["nombre"] = cursada.materia.materia.nombre
                actual["materia"]["siglas"] = cursada.materia.materia.siglas
                actual["materia"]["codigo"] = MateriaEnPlan.objects.filter(
                    materia=cursada.materia.materia)[0].codigo
                json_alumno["cursadas"].append(actual)
            for carrera in AlumnoDeCarrera.objects.filter(alumno=alumno):
                carrera_json = {}
                carrera_json["nombre"] = carrera.carrera.nombre
                carrera_json["codigo"] = carrera.carrera.codigo
                json_alumno["carreras"].append(carrera_json)
            json.append(json_alumno)
        return JsonResponse(json, safe=False)


class MateriasCursadasView(generics.ListAPIView):
    queryset = MateriaCursada.objects.none()
    serializer_class = MateriaCursadaSerializer

    def get_queryset(self):
        """
            - Chequeo permisos sobre esa carrera
            - Si tiene permisos, filtro las materias cursadas
        """
        try:
            carrera = Carrera.objects.get(codigo=self.kwargs['codigo_carrera'])
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            if carrera in carreras:
                return MateriaCursada.objects.filter(carrera=carrera)
        except:
            pass
        return MateriaCursada.objects.none()


class InscripcionesView(generics.ListAPIView):
    queryset = Inscripcion.objects.none()
    serializer_class = InscripcionSerializer

    def get_queryset(self):
        """
            - Chequeo permisos sobre esa carrera
            - Si tiene permisos, filtro las inscripciones
        """
        try:
            carrera = Carrera.objects.get(codigo=self.kwargs['codigo_carrera'])
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            if carrera in carreras:
                return Inscripcion.objects.filter(carrera=carrera)
        except:
            pass
        return Inscripcion.objects.none()


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


class AlumnosFiltradosPorCarreraView(generics.ListAPIView):
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


class AlumnosDeCarreraView(generics.ListAPIView):
    queryset = AlumnoDeCarrera.objects.none()
    serializer_class = AlumnoDeCarreraSerializer

    def get_queryset(self):
        """
        Retorna todos los alumnos de una determinada carrera,
        Si es que el usuario tiene permisos para ver esa carrera
        """
        alumnos = AlumnoDeCarrera.objects.none()
        try:
            carrera = Carrera.objects.get(codigo=self.kwargs['codigo_carrera'])
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            alumnos = AlumnoDeCarrera.objects.filter(carrera=carrera)
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


class PlanesDeCarreraView(generics.ListAPIView):
    queryset = PlanDeEstudio.objects.all()
    serializer_class = PlanDeEstudioSerializer

    def get_queryset(self):
        """
        Retorna todas las carreras que puede ver el usuario actual
        """
        planes = PlanDeEstudio.objects.none()
        try:
            carrera = Carrera.objects.get(codigo=self.kwargs['codigo_carrera'])
            profile = Profile.objects.get(user=self.request.user)
            carreras = profile.carreras.all()
            if carrera in carreras:
                planes = PlanDeEstudio.objects.filter(
                    carrera=carrera)
        except:
            pass
        return planes


class AlumnoMateriasCursadasView(generics.ListAPIView):
    queryset = MateriaCursada.objects.all()
    serializer_class = MateriaCursadaSerializer

    def get_queryset(self):
        """
            - Filtro las cursadas en base a las carreras que puede ver el usuario actual y el alumno
        """
        try:
            profile = Profile.objects.get(user=self.request.user)
            return MateriaCursada.objects.filter(carrera__in=profile.carreras.all(),
                                                 alumno__legajo=self.kwargs['legajo'])
        except:
            return MateriaCursada.objects.none()


class AlumnoInscripcionesView(generics.ListAPIView):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

    def get_queryset(self):
        """
            - Filtro las inscripciones en base a las carreras que puede ver el usuario actual
        """
        try:
            profile = Profile.objects.get(user=self.request.user)
            return Inscripcion.objects.filter(carrera__in=profile.carreras.all(),
                                              alumno__legajo=self.kwargs['legajo'])
        except:
            return Inscripcion.objects.none()


class MateriaAlumnosView(generics.ListAPIView):
    queryset = MateriaCursada.objects.all()
    serializer_class = MateriaCursadaSerializer

    def get_queryset(self):
        """
            - Filtro las cursadas en base a las carreras que puede ver el usuario actual
        """
        try:
            profile = Profile.objects.get(user=self.request.user)
            return MateriaCursada.objects.filter(carrera__in=profile.carreras.all(),
                                                 materia__materia__codigo=self.kwargs['codigo'])
        except:
            return MateriaCursada.objects.none()


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


class ImportarRequisitosView(ImportadorView):
    form = ImportarRequisitosForm
    template = 'importadores/importador_requisitos.html'


class ImportarPlanesView(ImportadorView):
    form = ImportarPlanesForm
    template = 'importadores/importador_planes.html'
