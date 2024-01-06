from django.utils.crypto import constant_time_compare
from django.http.request import split_domain_port

SESSION_KEY = '_store_accessed_id'
HASH_SESSION_KEY = '__store_accessed_hash'

CACHED_STORE = {}


def _get_site_by_request(request):
    host = request.get_host()
    from .models import Store
    try:
        # First attempt to look up the site by host with or without port.
        if host not in CACHED_STORE:
            CACHED_STORE[host] = Store.objects.get(
                user_id=request.user.id,
                domain__iexact=host
            )
        return CACHED_STORE[host]
    except Store.DoesNotExist:
        # Fallback to looking up site after stripping port from the host.
        domain, port = split_domain_port(host)
        if domain not in CACHED_STORE:
            CACHED_STORE[domain] = Store.objects.get(
                user_id=request.user.id,
                domain__iexact=domain
            )
        return CACHED_STORE[domain]


def get_current_store(request):
    store = _get_site_by_request(request)
    return store
