import graphene
from graphene_django.debug import DjangoDebug

from .builder import builder


class AppQuery(builder.Query, graphene.ObjectType):
    """root query"""
    debug = graphene.Field(DjangoDebug, name="_debug")


class AppMutation(builder.Mutation, graphene.ObjectType):
    """root mutation"""
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=AppQuery, mutation=AppMutation)
