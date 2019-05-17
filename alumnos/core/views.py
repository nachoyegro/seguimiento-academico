from .models import Persona, Alumno, Materia
from .serializers import PersonaSerializer, AlumnoSerializer, MateriaSerializer
from rest_framework import viewsets


class PersonasView(viewsets.ModelViewSet):
    """
    Provides a get method handler.
    """
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

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