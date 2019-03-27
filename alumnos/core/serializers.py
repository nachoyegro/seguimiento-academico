from rest_framework import serializers
from .models import *


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = ("nombre", "codigo")

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ("nombre", "apellido", "dni", "email")

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ("nombre", "codigo", "siglas")

class MateriaCursadaSerializer(serializers.ModelSerializer):
    materia = MateriaSerializer()
    class Meta:
        model = MateriaCursada
        fields = ("materia", "nota")

class AlumnoSerializer(serializers.HyperlinkedModelSerializer):
    datos_personales = PersonaSerializer()
    cursadas = MateriaCursadaSerializer(many=True)
    carreras = CarreraSerializer(many=True)
    class Meta:
        model = Alumno
        fields = ("datos_personales", "legajo", "es_regular", "cursadas", "carreras", "es_regular", "promedio")
