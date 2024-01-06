from typing import cast

import graphene
from graphene_django.debug import DjangoDebug

from .queries import UserQuery

queries_all = []


class AppQuery(UserQuery, graphene.ObjectType):
    """root query"""
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=AppQuery)

