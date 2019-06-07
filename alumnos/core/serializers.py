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

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ("id", "nombre", "apellido", "dni", "email")

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ("id", "nombre", "codigo", "siglas")

class MateriaCursadaSerializer(serializers.ModelSerializer):
    materia = MateriaSerializer()
    class Meta:
        model = MateriaCursada
        fields = ("id", "materia", "nota")

class AlumnoSerializer(serializers.HyperlinkedModelSerializer):
    datos_personales = PersonaSerializer()
    cursadas = MateriaCursadaSerializer(many=True, required=False)
    carreras = CarreraSerializer(many=True)

    def create(self, validated_data):
        datos_personales = validated_data.pop('datos_personales')
        persona = Persona.objects.create(**datos_personales)
        carreras_data = validated_data.pop('carreras')
        carreras_ids = [carrera['id'] for carrera in carreras_data]
        carreras = Carrera.objects.filter(id__in=carreras_ids)
        alumno = Alumno.objects.create(datos_personales=persona, **validated_data)
        for carrera in carreras:
            alumno.carreras.add(carrera)
        alumno.save()
        return alumno

    class Meta:
        model = Alumno
        fields = ("id", "datos_personales", "legajo", "es_regular", "cursadas", "carreras", "es_regular", "promedio")

class AlumnoInscripcionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    legajo = serializers.CharField(required=False)
    class Meta:
        model = Alumno
        fields = ("id", "legajo")

class InscripcionSerializer(serializers.ModelSerializer):
    alumno = serializers.PrimaryKeyRelatedField(queryset=Alumno.objects.all())
    comision = serializers.PrimaryKeyRelatedField(queryset=Comision.objects.all())
    class Meta:
        model = Inscripcion
        fields = ("id", "alumno", "comision")