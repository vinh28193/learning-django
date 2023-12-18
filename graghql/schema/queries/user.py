import graphene
import graphene_django_optimizer as gql_optimizer
from django.db.models import QuerySet

from graghql.nodes import UserNode
from user.models import User


class UserQuery(graphene.ObjectType):
    profile = graphene.Field(UserNode)

    @staticmethod
    def resolve_profile(root, info: graphene.ResolveInfo, **kwargs) -> QuerySet[User]:
        optimized_query = gql_optimizer.query(
            User.objects.filter(id=info.context.user.id), info
        )
        return optimized_query.first()
