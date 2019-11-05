from graphene_django import DjangoObjectType
import graphene
from .models import *


class MateriaNode(DjangoObjectType):
    class Meta:
        model = Materia


class AlumnoNode(DjangoObjectType):
    class Meta:
        model = Alumno


class MateriaEnPlanNode(DjangoObjectType):
    class Meta:
        model = MateriaEnPlan


class PlanDeEstudioNode(DjangoObjectType):
    class Meta:
        model = PlanDeEstudio


class CarreraNode(DjangoObjectType):
    class Meta:
        model = Carrera


class ProfesorNode(DjangoObjectType):
    class Meta:
        model = Profesor


class InscripcionNode(DjangoObjectType):
    class Meta:
        model = Inscripcion


class MateriaCursadaNode(DjangoObjectType):
    class Meta:
        model = MateriaCursada


class Query(graphene.ObjectType):
    materia = graphene.List(MateriaNode)
    alumno = graphene.List(AlumnoNode)
    materia_en_plan = graphene.List(MateriaEnPlanNode)
    plan_de_estudio = graphene.List(PlanDeEstudioNode)
    carrera = graphene.List(CarreraNode)
    profesor = graphene.List(ProfesorNode)
    inscripcion = graphene.List(InscripcionNode)
    materia_cursada = graphene.List(MateriaCursadaNode)

    def resolve_materia(self, info):
        return Materia.objects.all()

    def resolve_alumno(self, info):
        return Alumno.objects.all()

    def resolve_materia_en_plan(self, info):
        return MateriaEnPlan.objects.all()

    def resolve_plan_de_estudio(self, info):
        return PlanDeEstudio.objects.all()

    def resolve_carrera(self, info):
        return Carrera.objects.all()

    def resolve_profesor(self, info):
        return Profesor.objects.all()

    def resolve_inscripcion(self, info):
        return Inscripcion.objects.all()

    def resolve_materia_cursada(self, info):
        return MateriaCursada.objects.all()


schema = graphene.Schema(query=Query)
