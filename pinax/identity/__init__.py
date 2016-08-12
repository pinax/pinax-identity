import pkg_resources


__version__ = pkg_resources.get_distribution("pinax-identity").version


from .authentication import TokenAuthentication  # noqa
from .permissions import ensure_scope  # noqa
