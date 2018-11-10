from rest_framework import generics
from .models import Persona, Alumno
from .serializers import PersonaSerializer, AlumnoSerializer


class ListPersonasView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class ListAlumnosView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
