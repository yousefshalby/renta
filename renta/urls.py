from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from django.conf import settings
from django.conf.urls.static import static
from renta.swagger import CustomOpenAPISchemaGenerator

# Admin settings
admin.site.site_header = "Renta"
admin.site.site_title = "Renta site admin"
admin.site.index_title = "Renta site administration"


urlpatterns = [
    path('admin/', admin.site.urls),
]

# URL settings
main_patterns = i18n_patterns(
    path('api/', include("project.urls")),
)

urlpatterns += main_patterns


# swagger urls and configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Renta API",
        default_version="v1",
        description="Renta Swagger Documentation",
    ),
    public=True,
    # permission_classes=(permissions.IsAuthenticated,),
    # authentication_classes=(SessionAuthentication,),
    generator_class=CustomOpenAPISchemaGenerator,
    patterns=main_patterns,
)

urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
