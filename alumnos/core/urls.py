from django.urls import path, include
from .views import PersonasView, AlumnosView, MateriasView, ComisionView, CarrerasView
from rest_framework import routers, serializers, viewsets, generics

router = routers.DefaultRouter()
router.register(r'materias', MateriasView)
router.register(r'alumnos', AlumnosView)
router.register(r'personas', PersonasView)
router.register(r'comision', ComisionView)
router.register(r'carreras', CarrerasView)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
