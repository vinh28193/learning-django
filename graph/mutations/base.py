import graphene
from django.http import HttpRequest


class ResolverInfo(graphene.ResolveInfo):
    context: HttpRequest


class BaseMutation(graphene.relay.ClientIDMutation):
    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(
        cls, root, info: ResolverInfo, **data
    ) -> "BaseMutation":
        ...
