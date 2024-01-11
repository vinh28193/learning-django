import graphene
from copy import deepcopy
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer
from graphene_django.filter import DjangoFilterConnectionField


class BaseGraphModel:
    def __init__(self, model, builder):
        self.model = model
        self.builder = builder

# query resolver builders
def build_field_by_id_resolver(self):
    def field_resolver_function(root, info, **fields):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset, root, info, **fields)
        queryset = queryset.filter(pk=fields["id"])
        optimized_query = gql_optimizer.query(
            queryset, info, disable_abort_only=True
        )
        return optimized_query.first()
    return field_resolver_function

class GraphModel(BaseGraphModel):
    fields = None
    exclude = None
    filter_fields = ()
    connection = None
    connection_class = None
    use_connection = None
    interfaces = ()
    convert_choices_to_enum = True

    def setup(self):
        object_type = self.as_object_type()
        print("object_type", object_type)
        import graphene
        from graphene_django import DjangoObjectType
        from user.models import User

        class UserType(DjangoObjectType):
            class Meta:
                model = User
                exclude = ("password",)
                interfaces = (graphene.Node,)

        print(UserType, object_type)
        self.builder.types.append(object_type)
        object_name = self.model.__name__.lower()
        # build query
        setattr(
            self.builder.query, object_name,
            graphene.Field(object_type, id=graphene.ID(required=True))
        )
        func_id_resolver = build_field_by_id_resolver(self)
        setattr(
            self.builder.query, f'resolve_{object_name}',
            func_id_resolver
        )
        # setattr(
        #     self.builder.query, f"all_{object_name}",
        #     graphene.List(object_type, id=graphene.ID(required=False))
        # )
        # setattr(
        #     self.builder.query, f'resolve_all_{object_name}',
        #     self.resolve_all
        # )
        # build mutation

    def as_object_type(self):
        model_metaclass = type(f"Meta", (), {
            'model': self.model,
            'fields': self.fields,
            'exclude': self.exclude,
            'connection': self.connection,
            'interfaces': self.interfaces
        })
        print({
            'model': self.model,
            'fields': self.fields,
            'exclude': self.exclude,
            'connection': self.connection,
            'interfaces': self.interfaces
        })
        type_attrs = {'Meta': model_metaclass}
        object_type = type(
            f"{self.model.__name__}Type", (DjangoObjectType,),
            type_attrs
        )
        return object_type

    def get_queryset(self):
        return self.model.objects.all()

    def filter_queryset(self, queryset, root, info, **fields):
        return queryset



    def resolve_all(self, root, info, **fields):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset, root, info, **fields)

        optimized_query = gql_optimizer.query(
            queryset, info, disable_abort_only=True,
        )
        return optimized_query
