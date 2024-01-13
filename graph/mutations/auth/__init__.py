import graphene
import graphql_jwt

from .login import UserLoginMutation


class AuthMutation(graphene.ObjectType):
    login = UserLoginMutation.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
