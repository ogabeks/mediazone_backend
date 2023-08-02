from rest_framework import viewsets, mixins
from api import models, serializers, permissions


# ============= #
# MANAGER VIEWS #
# ============= #


# COMPANIES VIEWSET
class CompaniesViewset(viewsets.ModelViewSet):
    queryset = models.Company.objects.all().order_by('-id')
    serializer_class = serializers
    permission_classes = [permissions.ManagerLevelPermission]