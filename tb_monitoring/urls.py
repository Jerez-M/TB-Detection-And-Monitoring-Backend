from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="TB Monitoring API",
        default_version="v1",
        description="TB Monitoring API",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    authentication_classes=[],
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/v1/accounts/", include("accounts.urls")),
        path("api/v1/institutions/", include("institution.urls")),
        path("api/v1/administrators/", include("administrator.urls")),
        path("api/v1/patients/", include("patient.urls")),
        path("api/v1/tb_detections/", include("tb_detection.urls")),
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
