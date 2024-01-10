import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)
        interfaces = (graphene.Node,)
