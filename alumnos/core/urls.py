from django.urls import path, include
from .views import *
from rest_framework import routers, serializers, viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .token_serializer import AlumnosTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'carreras', CarrerasView)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/carreras/<str:codigo_carrera>/alumnos/',
         AlumnosDeCarreraView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/alumnos-completos/',
         AlumnosFiltradosPorCarreraView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/planes/<int:plan_anio>/',
         MateriasEnPlanView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/planes/',
         PlanesDeCarreraView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/materiascursadas/',
         MateriasCursadasView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/inscripciones/',
         InscripcionesView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/cantidad-graduados/',
         CantidadGraduadosView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/cantidad-graduados/<int:anio>/',
         CantidadGraduadosView.as_view()),
    path(r'api/alumno/<str:legajo>/cursadas/',
         AlumnoMateriasCursadasView.as_view()),
    path(r'api/alumno/<str:legajo>/inscripciones/',
         AlumnoInscripcionesView.as_view()),
    path(r'api/materia/<str:codigo>/alumnos/',
         MateriaAlumnosView.as_view()),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/v1/alumnos/', AlumnosAPIV1.as_view()),
    path(r'api/token/', AlumnosTokenObtainPairView.as_view(), name='token'),
    path(r'api/token/refresh/', TokenRefreshView.as_view()),
    path(r'admin/core/importar_materias_cursadas/',
         ImportarMateriasCursadasView.as_view()),
    path(r'admin/core/importar_alumnos/', ImportarDatosAlumnosView.as_view()),
    path(r'admin/core/importar_inscripciones/',
         ImportarInscripcionesView.as_view()),
    path(r'admin/core/importar_requisitos/',
         ImportarRequisitosView.as_view()),
    path(r'admin/core/importar_planes/',
         ImportarPlanesView.as_view()),
]
