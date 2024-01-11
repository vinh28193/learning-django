import graphene
import graph
from .models import User


@graph.register(User)
class UserGraphModel(graph.GraphModel):
    exclude = ("password",)
    interfaces = (graphene.relay.Node,)
