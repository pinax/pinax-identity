from django.conf.urls import url, include


urlpatterns = [
    url(r"^oidc/", include("oidc_provider.urls", namespace="oidc_provider")),
]
