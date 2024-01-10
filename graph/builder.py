import re

import graphene
from django.db.models.base import ModelBase
from .models import GraphModel


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class SchemaBuilder:

    def __init__(self):
        self._registry = {}  # model_class class -> graph class instance
        self.query = type("Query", (graphene.ObjectType,), {})
        self.mutation = type("Mutation", (graphene.ObjectType,), {})
        self.types = []

    def register(self, model_or_iterable, graph_class=None, **options):
        graph_class = graph_class or GraphModel
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                registered_graph = str(self._registry[model])
                msg = 'The model %s is already registered ' % model.__name__
                if registered_graph.endswith('.GraphModel'):
                    # Most likely registered without a ModelAdmin subclass.
                    msg += 'in app %r.' % re.sub(r'\.GraphModel', '', registered_graph)
                else:
                    msg += 'with %r.' % registered_graph
                raise AlreadyRegistered(msg)

            self._registry[model] = graph_class(model, self)

    def as_schema(self):
        for model in self._registry:
            graph_model = self._registry[model]
            graph_model.setup()

        return graphene.Schema(
            query=self.query, mutation=self.mutation, types=self.types
        )
