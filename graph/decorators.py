def register(*models, builder=None):
    """
    Register the given model(s) classes and wrapped ModelAdmin class with
    admin site:

    @register(Author)
    class AuthorGraph(graph.GraphModel):
        pass

    The `builder` kwarg is an admin site to use instead of the default admin site.
    """
    from .builder import SchemaBuilder, builder as default_builder
    from .models import GraphModel

    def _model_graph_wrapper(graph_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        graph_builder = builder or default_builder

        if not isinstance(graph_builder, SchemaBuilder):
            raise ValueError('site must subclass SchemaBuilder')

        if not issubclass(graph_class, GraphModel):
            raise ValueError('Wrapped class must subclass GraphModel.')

        graph_builder.register(models, graph_class=graph_class)

        return graph_class

    return _model_graph_wrapper
