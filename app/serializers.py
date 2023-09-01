from rest_framework.serializers import ModelSerializer, BooleanField, CharField, IntegerField, ListField
from . import models


class ProfileSerializer(ModelSerializer):
    level_display = CharField(source='get_level_display', read_only=True)
    bonus = IntegerField(source='bonus_amount', read_only=True)
    fine = IntegerField(source='fine_amount', read_only=True)
    debt = IntegerField(source='debt_amount', read_only=True)
    attendace = IntegerField(source='attendace_amount', read_only=True)
    grs = ListField(source='groups', read_only=True)

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
    students = StudentSerializer(many=True)
    teacher_name = CharField(source='teacher.name', read_only=True)
    students_count = CharField(source='students.count', read_only=True)
    unpayments_count = CharField(source='unpayments', read_only=True)
    status = CharField(source='students_status', read_only=True)

    class Meta:
        fields = '__all__'
        model = models.Group


class SubscriptionSerializer(ModelSerializer):
    group_name = CharField(source='group.name', read_only=True)
    month_name = CharField(source='month.month', read_only=True)
    student_name = CharField(source='student.name', read_only=True)

    class Meta:
        fields = ('__all__')
        model = models.Subscription


class CompanySettingsSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.CompanySettings


class TeacherBonusSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
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


class CompanySettingsSerializer(ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = models.CompanySettings
