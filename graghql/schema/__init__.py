from typing import cast

import graphene
from graphene_django.debug import DjangoDebug

from .queries import UsersQuery

queries_all = []


class AppQuery(UsersQuery):
    """root query"""
    # debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=cast(graphene.ObjectType, AppQuery))
