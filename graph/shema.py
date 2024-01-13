from typing import cast

import graphene
from graphene_django.debug import DjangoDebug

from .queries import UserQuery

from .mutations import AuthMutation

queries_all = []


class AppQuery(UserQuery, graphene.ObjectType):
    """root query"""
    debug = graphene.Field(DjangoDebug, name="_debug")


class AppMutation(AuthMutation, graphene.Mutation):
    """root mutation"""
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=AppQuery, mutation=AppMutation)

__all__ = ["schema"]
