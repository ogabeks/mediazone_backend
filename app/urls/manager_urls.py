from rest_framework.routers import SimpleRouter
from app import views

urlpatterns = []
router = SimpleRouter()


router.register('companies', views.CompaniesViewset)

urlpatterns += router.urls
