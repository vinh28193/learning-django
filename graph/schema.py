from typing import cast

import graphene
from graphene_django.debug import DjangoDebug
from .queries import *  # noqa
from .queries import __all__ as queries  # noqa
from .mutations import *  # noqa
from .mutations import __all__ as mutations  # noqa

AppQuery = type(
    "AppQuery", tuple(eval(query) for query in queries), {
        "debug": graphene.Field(DjangoDebug, name="_debug")
    }
)

AppMutation = type(
    "AppMutation", tuple(eval(mutation) for mutation in mutations), {}
)

schema = graphene.Schema(
    query=cast(graphene.ObjectType, AppQuery), mutation=AppMutation
)
