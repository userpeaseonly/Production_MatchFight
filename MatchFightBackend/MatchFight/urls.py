from django.contrib import admin
from django.urls import path, include
from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('competitions.urls')),
    path('api/', include('tournaments.urls')),
    path('api/', include('participants.urls')),
    path('api/', include('matches.urls')),
    path('api/', include('finals.urls')), 
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
