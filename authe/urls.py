from django.urls import path
from authe.views import create_user_view,login_view, me_view
from config.urls import schema_view

urlpatterns = [
    path('create_user/', create_user_view),
    path('login/', login_view),
    path('me/', me_view)
]

path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),