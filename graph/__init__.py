from django.utils.module_loading import autodiscover_modules
from .models import GraphModel
from .decorators import register

from .builder import builder

__all__ = [
    "register", "builder", "autodiscover", "GraphModel"
]


def autodiscover():
    autodiscover_modules('graph', register_to=builder)


default_app_config = 'graph.apps.GraphConfig'
