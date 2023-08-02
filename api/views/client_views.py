from rest_framework import viewsets, mixins
from api import models, permissions, serializers


# ================================ #
# ADMIN, CASHER AND TEACHER VIEWS  #
# ================================ #

# PROFILES VIEWSET
class ProfileViewset(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,  viewsets.GenericViewSet):
    permission_classes = [permissions.ProfileLevelPermission, permissions.OwnerPermission]
    queryset = models.Profile.objects.all().order_by('-id')
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        pk = self.kwargs.get('pk')
        if pk is not None:
            queryset = queryset.filter(user__pk=pk)

        return queryset
    
    


# COMPANIES VIEWSET
class CompanyViewset(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.ProfileLevelPermission, permissions.OwnerPermission]
    queryset = models.Company.objects.all().order_by('-id')
    serializer_class = serializers.CompanySerializer


# COMPANIES SUBSCRIPTIONS
class CompanySubsciptionViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AdminLevelPermission, permissions.OwnerPermission]
    queryset = models.CompanySubscription.objects.all().order_by('-id')
    serializer_class = serializers.CompanySubscriptionSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset



# SUBJECTS VIEWSET
class SubjectViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.ProfileLevelPermission]
    queryset = models.Subject.objects.all().order_by('-id')
    serializer_class = serializers.SubjectSerializer


# STUDENTS VIEWSET
class StudentViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.Student.objects.all().order_by('-id')
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset


# GROUP VIEWSET
class GroupViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.Group.objects.all().order_by('-id')
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset


# SUBSCRIPTION VIEWSET
class SubscriptionViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset
    

# COMPANY SETTINGS
class CompanySettingsViewset(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AdminLevelPermission, permissions.OwnerPermission]
    queryset = models.CompanySettings.objects.all()
    serializer_class = serializers.CompanySettingsSerializer


# TEACHERS BONUSES VIEWSET
class TeacherBonusViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.TeacherBonus.objects.all()
    serializer_class = serializers.TeacherBonusSerializer


    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset
    

# TEACHERS ATTTENDACES VIEWSET
class TeacherAttendaceViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.TeacherAttendace.objects.all()
    serializer_class = serializers.TeacherAttendaceSerializer


    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset
    

# TEACHERS FINES VIEWSET
class TeacherFinesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.TeacherFine.objects.all()
    serializer_class = serializers.TeacherFineSerializer


    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset
    


# TEACHERS DEBTS VIEWSET
class TeacherDebtsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission, permissions.OwnerPermission]
    queryset = models.TeacherDebt.objects.all()
    serializer_class = serializers.TeacherDebtSerializer


    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset
    



# TEACHERS DEBTS VIEWSET
class ExpensesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.ProfileLevelPermission, permissions.OwnerPermission]
    queryset = models.Expense.objects.all()
    serializer_class = serializers.ExpenseSerializer


    def get_queryset(self):
        queryset =  super().get_queryset()
        user = self.request.user
        
        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None
        
        return queryset