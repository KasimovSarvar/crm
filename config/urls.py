
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from drf_yasg import openapi

from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Marketplace api and payment",
        default_version="v1",
        description="API for backend ",
        terms_of_service="22",
        contact=openapi.Contact(email="@usmanismailov"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("authe.urls")),

]

urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        )
    ]



urlpatterns+=static(settings.MEDIA_URL,serve, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,serve, document_root=settings.STATIC_ROOT)
