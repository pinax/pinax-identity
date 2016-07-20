## Installation

Add to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        "pinax.identity",
        "oidc_provider",
        ...
    ]

Add to urls.py:

    urlpatterns = [
        ...
        url(r"", include("pinax.identity.urls")),
        ...
    ]

Most likely you'll need to handle CORS, use django-cors-headers. Add the
middleware to the top of MIDDLEWARE_CLASSES:

    MIDDLEWARE_CLASSES = [
        "corsheaders.middleware.CorsMiddleware",
        ...
    ]

Add to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        "corsheaders",
        ...
    ]

Add settings:

    CORS_ORIGIN_WHITELIST = [
        "localhost:5000"  # change this for your client
    ]
