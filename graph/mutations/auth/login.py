import graphene
import graphql_jwt

from graph.types import UserType


class UserLoginMutation(graphql_jwt.relay.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments['input']._meta.fields.update({
            'store_id': graphene.InputField(graphene.Int, required=True),
        })
        return super().Field(*args, **kwargs)

    @classmethod
    def resolve(cls, _, info, **kwargs):
        return cls(user=info.context.user)  # noqa
