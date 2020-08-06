from django.urls import path, include
from django.conf.urls import url
from .views import *
from rest_framework import routers, serializers, viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .token_serializer import AlumnosTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'carreras', CarrerasView)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'carreras/<str:codigo_carrera>/alumnos/',
         AlumnosDeCarreraView.as_view()),
    path(r'carreras/<str:codigo_carrera>/alumnos-completos/',
         AlumnosFiltradosPorCarreraView.as_view()),
    path(r'carreras/<str:codigo_carrera>/planes/<int:plan_anio>/',
         MateriasEnPlanView.as_view()),
    path(r'carreras/<str:codigo_carrera>/planes/<int:plan_anio>/cantidad-materias-necesarias/',
         MateriasNecesariasView.as_view()),
    path(r'carreras/<str:codigo_carrera>/planes/',
         PlanesDeCarreraView.as_view()),
    path(r'carreras/<str:codigo_carrera>/materiascursadas/',
         MateriasCursadasView.as_view()),
    path(r'carreras/<str:codigo_carrera>/inscripciones/',
         InscripcionesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/inscripciones/<int:anio>/<int:semestre>/',
         InscripcionesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-graduados/',
         CantidadGraduadosView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-graduados/<int:anio>/',
         CantidadGraduadosView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-cursantes/',
         CantidadCursantesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-cursantes/<int:anio>/',
         CantidadCursantesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-ingresantes/',
         CantidadIngresantesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-ingresantes/<int:anio>/',
         CantidadIngresantesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-postulantes/<int:anio>/',
         CantidadPostulantesView.as_view()),
    path(r'carreras/<str:codigo_carrera>/cantidad-postulantes/',
         CantidadPostulantesView.as_view()),
    path(r'alumno/<str:legajo>/cursadas/',
         AlumnoMateriasCursadasView.as_view()),
    path(r'alumno/<str:legajo>/inscripciones/',
         AlumnoInscripcionesView.as_view()),
    path(r'materia/<str:codigo>/alumnos/',
         MateriaAlumnosView.as_view()),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'v1/alumnos/', AlumnosAPIV1.as_view()),
    path(r'token/', AlumnosTokenObtainPairView.as_view(), name='token'),
    path(r'token/refresh/', TokenRefreshView.as_view()),
]
