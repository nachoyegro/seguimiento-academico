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

class MateriaCursadaSerializer(serializers.ModelSerializer):
    materia = MateriaSerializer()
    class Meta:
        model = MateriaCursada
        fields = ("id", "materia", "nota")

class AlumnoSerializer(serializers.HyperlinkedModelSerializer):
    cursadas = MateriaCursadaSerializer(many=True, required=False)

    def create(self, validated_data):
        carreras_data = validated_data.pop('carreras')
        carreras_ids = [carrera['id'] for carrera in carreras_data]
        carreras = Carrera.objects.filter(id__in=carreras_ids)
        alumno = Alumno.objects.create(**validated_data)
        for carrera in carreras:
            alumno.carreras.add(carrera)
        alumno.save()
        return alumno

    class Meta:
        model = Alumno
        fields = ("id", "nombre", "apellido", "email", "legajo", "es_regular", "cursadas", "es_regular")
