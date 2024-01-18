import graphene
import graphene_django_optimizer as gql_optimizer
from graphene_django import DjangoConnectionField
from django.db.models import QuerySet
from graph.types import UserType
from store.models import Store


class StoreQuery(graphene.ObjectType):
    store = graphene.Field(UserType, id=graphene.ID(required=True))
    all_store = DjangoConnectionField(UserType)

    @staticmethod
    def resolve_store(root, info, **kwargs) -> QuerySet[Store]:
        optimized_query = gql_optimizer.query(
            Store.objects.filter(id=kwargs["id"]), info
        )
        return optimized_query.first()

    @classmethod
    def resolve_all_users(cls, root, info, **kwargs) -> QuerySet[Store]:
        return gql_optimizer.query(
            Store.objects.all(), info, disable_abort_only=True
        )
