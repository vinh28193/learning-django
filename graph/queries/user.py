import graphene
import graphene_django_optimizer as gql_optimizer
from graphene_django import DjangoConnectionField
from django.db.models import QuerySet
from graph.types import UserType
from user.models import User


class UserQuery(graphene.ObjectType):
    profile = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    all_users = DjangoConnectionField(UserType)

    @staticmethod
    def resolve_profile(root, info, **kwargs) -> QuerySet[User]:
        optimized_query = gql_optimizer.query(
            User.objects.filter(id=info.context.user.id), info
        )
        return optimized_query.first()

    @staticmethod
    def resolve_user(root, info, **kwargs) -> QuerySet[User]:
        optimized_query = gql_optimizer.query(
            User.objects.filter(id=kwargs["id"]), info
        )
        return optimized_query.first()

    @classmethod
    def resolve__all_users(cls, root, info, **kwargs) -> QuerySet[User]:
        return gql_optimizer.query(
            User.objects.all(), info, disable_abort_only=True
        )
