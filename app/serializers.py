from rest_framework.serializers import ModelSerializer, BooleanField, CharField
from . import models

class ProfileSerializer(ModelSerializer):
    level_display = CharField(source='get_level_display', read_only=True)
    class Meta:
        fields = ('__all__')
        model = models.Profile


class CompanySerializer(ModelSerializer):
    is_active = BooleanField(source='is_subscribed', read_only=True)

    class Meta:
        fields = ('__all__')
        model = models.Company


class CompanySubscriptionSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.CompanySubscription


class SubjectSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.Subject


class StudentSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Student


class GroupSerializer(ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    
    class Meta:
        fields = '__all__'
        model = models.Group


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.Subscription


class CompanySettingsSerializer(ModelSerializer):
    class Meta:
        fields =  ('__all__')
        model = models.CompanySettings


class TeacherBonusSerializer(ModelSerializer):
    class Meta:
        fields =  ('__all__')
        model = models.TeacherBonus

class TeacherAttendaceSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TeacherAttendace


class TeacherFineSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TeacherFine


class TeacherDebtSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.TeacherDebt


class ExpenseSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.Expense