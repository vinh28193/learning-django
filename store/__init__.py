from django.utils.crypto import constant_time_compare

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'


def get_store_model():
    from store.models import Store
    return Store


def _get_session_key(request):
    # This value in the session is always serialized to a string, so we need
    # to convert it back to Python whenever we access it.
    return get_store_model()._meta.pk.to_python(request.session[SESSION_KEY])


def access(request, store):
    session_hash = ''
    if store is None:
        store = request.store
    if hasattr(store, 'get_session_hash'):
        session_hash = store.get_session_hash()

    if SESSION_KEY in request.session:
        if _get_session_key(request) != store.pk or (
            session_hash and
            not constant_time_compare(
                request.session.get(HASH_SESSION_KEY, ''),
                session_hash
            )
        ):
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()

    request.session[SESSION_KEY] = store._meta.pk.value_to_string(store)
    request.session[HASH_SESSION_KEY] = session_hash
    if hasattr(request, 'store'):
        request.store = store


def get_store_accessed(request):
    store = None
    try:
        store_id = _get_session_key(request)
    except KeyError:
        pass
    else:
        from .models import Store

        try:
            store = Store.objects.get(pk=store_id)
        except Store.DoesNotExist:
            pass
        else:
            # Verify the session
            if hasattr(store, 'get_session_hash'):
                session_hash = request.session.get(HASH_SESSION_KEY)
                session_hash_verified = session_hash and constant_time_compare(
                    session_hash,
                    store.get_session_hash()
                )
                if not session_hash_verified:
                    if not (
                        session_hash and
                        hasattr(store, '_legacy_get_session_hash') and
                        constant_time_compare(
                            session_hash, store._legacy_get_session_hash()
                        )
                    ):
                        request.session.flush()
                        store = None
    return store
