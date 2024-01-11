from django.apps import AppConfig


class SimpleGraphConfig(AppConfig):
    name = 'graph'

    def ready(self):
        self.module.autodiscover()


class GraphConfig(SimpleGraphConfig):
    """The default AppConfig for admin which does autodiscovery."""

    def ready(self):
        super().ready()
        self.module.autodiscover()
