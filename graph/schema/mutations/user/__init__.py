import graphene
import graphql_jwt

from .auth import UserLoginMutation


class UsersMutation(graphene.ObjectType):
    login = UserLoginMutation.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
