from django.urls import path, include
from .views import *
from rest_framework import routers, serializers, viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .token_serializer import AlumnosTokenObtainPairView

router = routers.DefaultRouter()
router.register(r'materias', MateriasView)
router.register(r'alumnos', AlumnosView)
router.register(r'carreras', CarrerasView)
#router.register(r'materiascursadas', MateriasCursadasView)
#router.register(r'inscripciones', InscripcionesView)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/carreras/<str:codigo_carrera>/alumnos/',
         AlumnosDeCarreraView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/planes/<int:plan_anio>/',
         MateriasEnPlanView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/materiascursadas/',
         MateriasCursadasView.as_view()),
    path(r'api/carreras/<str:codigo_carrera>/inscripciones/',
         InscripcionesView.as_view()),
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
