import graphene
from copy import deepcopy
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer
from graphene_django.filter import DjangoFilterConnectionField


class BaseGraphModel:
    def __init__(self, model, builder):
        self.model = model
        self.builder = builder


class GraphModel(BaseGraphModel):
    fields = "__all__"
    filter_fields = "__all__"
    connection = None
    connection_class = None
    use_connection = None
    interfaces = ()
    convert_choices_to_enum = True

    def setup(self):
        object_type = self.as_object_type()
        object_name = self.model.__name__.lower()
        # build query
        setattr(
            self.builder.Query, object_name,
            graphene.Field(object_type, id=graphene.ID())
        )
        setattr(
            self.builder.Query, f'resolve_{object_name}',
            self.resolve_one
        )
        setattr(
            self.builder.Query, f"all_{object_name}",
            DjangoFilterConnectionField(object_type)
        )
        setattr(
            self.builder.Query, f'resolve_all_{object_name}',
            self.resolve_all
        )
        # build mutation

    def as_object_type(self):
        model_metaclass = type(f"Meta", (), {
            'model': self.model,
            'fields': self.fields,
            'filter_fields': self.filter_fields,
            'interfaces': self.interfaces
        })
        type_attrs = {'Meta': model_metaclass}
        object_type = type(
            f"{self.model.__name__}Type", (DjangoObjectType,),
            type_attrs
        )
        self.builder.types.append(object_type)
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

    def resolve_one(self, root, info, **fields):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset, root, info, **fields)
        queryset = queryset.filter(pk=1)
        optimized_query = gql_optimizer.query(
            queryset, info, disable_abort_only=True
        )
        return optimized_query.first()
