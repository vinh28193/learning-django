import graphene
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer
from graphene_django.filter import DjangoFilterConnectionField


class BaseGraphModel:
    def __init__(self, model, builder):
        self.model = model
        self.builder = builder


class GraphModel(BaseGraphModel):
    class Meta:
        fields = None
        exclude = None
        filter_fields = {}
        connection = None
        connection_class = None
        use_connection = None
        interfaces = ()
        convert_choices_to_enum = True

    def setup(self):
        object_type = self.as_object_type()
        self.builder.types.append(object_type)
        object_name = self.model.__name__.lower()
        # build query
        setattr(
            self.builder.query, object_name,
            graphene.Field(object_type, id=graphene.ID(required=True))
        )
        setattr(
            self.builder.query, f'resolve_{object_name}',
            self.resolve_one
        )
        setattr(
            self.builder.query, f"all_{object_name}",
            DjangoFilterConnectionField(object_type)
        )
        setattr(
            self.builder.query, f'resolve_all_{object_name}',
            self.resolve_all
        )
        # build mutation

    def as_object_type(self):
        type_attrs = {'Meta': self.Meta}
        return type(
            f"{self.model.__name__}Type", (DjangoObjectType,),
            type_attrs
        )

    def get_queryset(self):
        return self.model.objects.all()

    def filter_queryset(self, queryset, root, info, **fields):
        return queryset

    def resolve_one(self, root, info, **fields):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset, root, info, **fields)
        queryset = queryset.filter(pk=fields["pk"])
        optimized_query = gql_optimizer.query(
            queryset, info, disable_abort_only=True
        )
        return optimized_query.first()

    def resolve_all(self, root, info, **fields):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset, root, info, **fields)

        optimized_query = gql_optimizer.query(
            queryset, info, disable_abort_only=True,
        )
        return optimized_query
