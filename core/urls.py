from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('app.urls.general')),
    path('api/v1/client/', include('app.urls.client_urls')),
    path('api/v1/manager/', include('app.urls.manager_urls')),
    path('', TemplateView.as_view(template_name='index.html')),

]
