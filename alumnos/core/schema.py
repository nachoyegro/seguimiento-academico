from graphene_django import DjangoObjectType
import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from .models import *
from django.contrib.auth.models import User

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class UserNode(DjangoObjectType):
    class Meta:
        model = User

class MateriaNode(DjangoObjectType):
    class Meta:
        model = Materia

class AlumnoNode(DjangoObjectType):
    class Meta:
        model = AlumnoDeCarrera

class ComisionNode(DjangoObjectType):
    class Meta:
        model = Comision

class MateriaEnPlanNode(DjangoObjectType):
    class Meta:
        model = MateriaEnPlan

class PlanDeEstudioNode(DjangoObjectType):
    class Meta:
        model = PlanDeEstudio

class CarreraNode(DjangoObjectType):
    class Meta:
        model = Carrera

class MateriaCursadaNode(DjangoObjectType):
    class Meta:
        model = MateriaCursada

class Query(graphene.ObjectType):
    viewer = graphene.Field(UserNode, token=graphene.String(required=True))
    materias = graphene.List(MateriaNode)
    materia = graphene.Field(MateriaNode, id=graphene.Int())
    alumnos = graphene.List(AlumnoNode)
    alumno = graphene.Field(AlumnoNode, id=graphene.Int())
    comisiones = graphene.List(ComisionNode)
    materias_en_plan = graphene.List(MateriaEnPlanNode)
    planes_de_estudio = graphene.List(PlanDeEstudioNode)
    carreras = graphene.List(CarreraNode)
    carrera = graphene.Field(CarreraNode, id=graphene.Int())
    materias_cursadas = graphene.List(MateriaCursadaNode)

    @login_required
    def resolve_viewer(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        return user

    @login_required
    def resolve_materias(self, info):
        return Materia.objects.all()

    @login_required
    def resolve_materia(self, info, **kwargs):
        id = kwargs.get('id')
        if id:
            return Materia.objects.get(pk=id)
        return None

    @login_required
    def resolve_alumnos(self, info):
        return AlumnoDeCarrera.objects.all()

    @login_required
    def resolve_alumno(self, info, **kwargs):
        id = kwargs.get('id')
        if id:
            return AlumnoDeCarrera.objects.get(pk=id)
        return None

    @login_required
    def resolve_comisiones(self, info):
        return Comision.objects.all()

    @login_required
    def resolve_materias_en_plan(self, info):
        return MateriaEnPlan.objects.all()

    @login_required
    def resolve_planes_de_estudio(self, info):
        return PlanDeEstudio.objects.all()

    @login_required
    def resolve_carreras(self, info):
        return Carrera.objects.all()

    @login_required
    def resolve_carrera(self, info, **kwargs):
        id = kwargs.get('id')
        if id:
            return Carrera.objects.get(pk=id)
        return None

    @login_required
    def resolve_materias_cursadas(self, info):
        return MateriaCursada.objects.all()