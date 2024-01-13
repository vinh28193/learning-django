from typing import cast

import graphene
from graphene_django.debug import DjangoDebug

from .queries import UserQuery

from .mutations import AuthMutation


class AppQuery(UserQuery, graphene.ObjectType):
    """root query"""
    debug = graphene.Field(DjangoDebug, name="_debug")


class AppMutation(AuthMutation):
    """root mutation"""


schema = graphene.Schema(
    query=cast(graphene.ObjectType, AppQuery), mutation=AppMutation
)
