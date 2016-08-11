import pkg_resources


__version__ = pkg_resources.get_distribution("pinax-identity").version


from . import authentication, permissions  # noqa
