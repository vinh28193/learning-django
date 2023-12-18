import graphene
import graphql_jwt

from graghql.nodes import UserNode


class UserLoginMutation(graphql_jwt.relay.JSONWebTokenMutation):
    user = graphene.Field(UserNode)

    @classmethod
    def resolve(cls, _, info, **kwargs):
        return cls(user=info.context.user)  # noqa
