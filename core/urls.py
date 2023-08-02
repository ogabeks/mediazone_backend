from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls.general')),
    path('api/v1/client/', include('api.urls.client_urls')),
    path('api/v1/manager/', include('api.urls.manager_urls')),
]
