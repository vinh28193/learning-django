import graphene
from graphene_django import DjangoObjectType
from store.models import Store


class StoreType(DjangoObjectType):
    class Meta:
        model = Store
        interfaces = (graphene.Node,)


__all__ = ["StoreType"]
