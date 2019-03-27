import core.schema
import graphene
from graphene_django.debug import DjangoDebug


class Query(core.schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)
