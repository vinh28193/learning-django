from graphene import ClientIDMutation


class BaseMutation(ClientIDMutation):
    class Meta:
        abstract = True
