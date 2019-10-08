from rest_framework import serializers
from .models import *

class ComisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comision
        fields = ("id", "materia", "nombre")

class CarreraSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(required=False)
    codigo = serializers.CharField(required=False)
    class Meta:
        model = Carrera
        fields = ("id", "nombre", "codigo")

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ("id", "nombre", "siglas")

class MateriaEnPlanSerializer(serializers.ModelSerializer):
    materia = serializers.SlugRelatedField(read_only=True, slug_field="nombre")
    plan = serializers.SlugRelatedField(read_only=True, slug_field="anio")
    class Meta:
        model = MateriaEnPlan 
        fields = ("id", "materia", "nombre_en_plan", "plan")

class MateriaCursadaSerializer(serializers.ModelSerializer):
    materia = MateriaEnPlanSerializer()
    alumno = serializers.SlugRelatedField(read_only=True, slug_field="legajo")
    carrera = serializers.SlugRelatedField(read_only=True, slug_field="codigo")
    class Meta:
        model = MateriaCursada
        fields = ("id", "materia", "nota", "alumno", "carrera", "fecha", "resultado")

class AlumnoSerializer(serializers.HyperlinkedModelSerializer):
    cursadas = MateriaCursadaSerializer(many=True, required=False)
    
    class Meta:
        model = Alumno
        fields = ("id", "nombre", "apellido", "email", "legajo", "es_regular", "cursadas", "es_regular")
