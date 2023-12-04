from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


def get_access_store(request):
    if not hasattr(request, '_cached_store'):
        from store import get_store_accessed
        request._cached_store = get_store_accessed(request)
        print("re", request.__class__.__name__)
    return request._cached_store


class StoreAccessMiddleware(MiddlewareMixin):

    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'store.contrib.middleware.StoreAccessMiddleware'."
        )
        request.store = SimpleLazyObject(lambda: get_access_store(request))
