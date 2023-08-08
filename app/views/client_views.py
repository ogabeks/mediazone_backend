from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from app import models, permissions, serializers
from django.utils import timezone
from datetime import datetime


current_month = timezone.now().month
current_year = timezone.now().year


# ================================ #
# ADMIN, CASHER AND TEACHER VIEWS  #
# ================================ #

# PROFILES VIEWSET
class ProfileViewset(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,  viewsets.GenericViewSet):
    permission_classes = [
        permissions.ProfileLevelPermission, permissions.OwnerPermission]
    queryset = models.Profile.objects.all().order_by('-id')
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
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
    permission_classes = [
        permissions.ProfileLevelPermission, permissions.OwnerPermission]
    queryset = models.Company.objects.all().order_by('-id')
    serializer_class = serializers.CompanySerializer


# COMPANIES SUBSCRIPTIONS
class CompanySubsciptionViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        permissions.AdminLevelPermission, permissions.OwnerPermission]
    queryset = models.CompanySubscription.objects.all().order_by('-id')
    serializer_class = serializers.CompanySubscriptionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
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
class StudentViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.Student.objects.all().order_by('-id')
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company, status='1')
        except:
            return None

        return queryset


# GROUP VIEWSET
class GroupViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.Group.objects.all().order_by('-id')
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


# SUBSCRIPTION VIEWSET
class SubscriptionViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.ProfileLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


# COMPANY SETTINGS
class CompanySettingsViewset(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        permissions.AdminLevelPermission, permissions.OwnerPermission]
    queryset = models.CompanySettings.objects.all()
    serializer_class = serializers.CompanySettingsSerializer


# TEACHERS BONUSES VIEWSET
class TeacherBonusViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.TeacherBonus.objects.all()
    serializer_class = serializers.TeacherBonusSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


# TEACHERS ATTTENDACES VIEWSET
class TeacherAttendaceViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.TeacherAttendace.objects.all()
    serializer_class = serializers.TeacherAttendaceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


# TEACHERS FINES VIEWSET
class TeacherFinesViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.TeacherFine.objects.all()
    serializer_class = serializers.TeacherFineSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


# TEACHERS DEBTS VIEWSET
class TeacherDebtsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.TeacherDebt.objects.all()
    serializer_class = serializers.TeacherDebtSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


# TEACHERS DEBTS VIEWSET
class ExpensesViewset(viewsets.ModelViewSet):
    permission_classes = [
        permissions.ProfileLevelPermission, permissions.OwnerPermission]
    queryset = models.Expense.objects.all()
    serializer_class = serializers.ExpenseSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)
        except:
            return None

        return queryset


@api_view(["POST"])
@permission_classes([permissions.ProfileLevelPermission])
def check_student(request):
    post_data = request.data
    barcode = post_data.get('barcode')

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
        student = models.Student.objects.get(
            company=company, student_id=barcode, status=1)
    except:
        return Response("O'quvchi topilmadi", status=status.HTTP_404_NOT_FOUND)

    groups = models.Group.objects.filter(
        students=student, company=company, status=1)

    all_subscription = []

    current_month_subscriptions = []
    current_month_groups = []

    months = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun',
              'Iyul', 'Avgust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr']
    for group in groups:
        try:
            group_teacher = group.teacher.name
        except:
            group_teacher = 'mavjud emas'

        subscription_by_group = {'group_id': group.id,
                                 'group_name': group.name, 'group_cost': group.cost, 'group_teacher': group_teacher, 'months': []}
        subscriptions = models.Subscription.objects.filter(
            company=company, student=student, group=group, month__year=current_year, status=1)

        get_current_month = subscriptions.filter(
            month__year=current_year, month__month=current_month)

        if len(get_current_month) == 0:

            try:
                teacher_phone = group.teacher.phone
            except:
                teacher_phone = 'mavjud emas'

            try:
                group_subject = group.subject.name
            except:
                group_subject = 'Mavjud emas'

            current_month_groups.append({'group_id': group.id, 'group_cost': group.cost, 'group_name': group.name, 'subject': group_subject,
                                        'teacher_name': group_teacher, 'teacher_phone': teacher_phone})

        for scm in get_current_month:
            if scm.group == group:
                current_month_subscriptions.append(True)
            else:
                current_month_subscriptions.append(False)

        for i in range(1, 13):
            if len(subscriptions) > 0:
                is_subscribed = subscriptions.filter(month__month=i).exists()
                if (is_subscribed):
                    s = {'month': i, 'month_name': months[i-1], 'status': True}
                else:
                    s = {'month': i,
                         'month_name': months[i-1], 'status': False}

            else:
                s = {'month': i, 'month_name': months[i-1], 'status': False}
            subscription_by_group['months'].append(s)
        all_subscription.append(subscription_by_group)

    if sum(current_month_subscriptions) == len(groups):
        active = True
    else:
        active = False

    if len(groups) > 0:
        has_groups = True
    else:
        has_groups = False

    serializer = serializers.StudentSerializer(student).data
    student_info = {'student': serializer,
                    'subscriptions': all_subscription, 'suspended': current_month_groups}

    return Response({"success": True, 'active': active, 'has_groups': has_groups, 'student_info': student_info})


@api_view(['POST'])
@permission_classes([permissions.ProfileLevelPermission])
def is_subscribed(request):
    data = request.data
    month = int(data.get('month'))
    group_id = data.get('group_id')
    student_id = data.get('student_id')

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    try:
        group = models.Group.objects.get(
            id=group_id, company=company, status='1')
    except:
        return Response("Guruh topilmadi", status=status.HTTP_404_NOT_FOUND)

    try:
        student = models.Student.objects.get(
            student_id=student_id, company=company, status='1')
    except:
        return Response("O'quvchi topilmadi", status=status.HTTP_404_NOT_FOUND)

    check_in = group.students.filter(id=student.id).exists()

    if check_in != True:
        return Response("O'quvchi ushbu guruhga a'zo emas", status=status.HTTP_400_BAD_REQUEST)

    subs = models.Subscription.objects.filter(
        company=company, group=group, student=student, month__month=month, month__year=current_year).exists()

    return Response(subs, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.ProfileLevelPermission])
def add_subscription(request):
    data = request.data
    group_id = data.get('group_id')
    student_id = data.get('student_id')
    amount = data.get('amount')

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    try:
        group = models.Group.objects.get(
            id=group_id, company=company, status='1')
    except Exception as e:
        print(e, company)
        print(group_id, student_id, amount)
        return Response("Guruh topilmadi", status=status.HTTP_404_NOT_FOUND)

    try:
        student = models.Student.objects.get(
            student_id=student_id, company=company, status='1')
    except:
        return Response("O'quvchi topilmadi", status=status.HTTP_404_NOT_FOUND)

    try:
        amount = int(amount)
    except:
        return Response("Parametr qiymatlari xato", status=status.HTTP_400_BAD_REQUEST)

    try:
        month = int(data.get('month'))
    except:
        month = False

    check_in = group.students.filter(id=student.id).exists()

    if check_in != True:
        return Response("O'quvchi ushbu guruhga a'zo emas", status=status.HTTP_400_BAD_REQUEST)

    subs = models.Subscription.objects.filter(
        company=company, group=group, student=student, month__month=month, month__year=current_year).exists()

    if subs:
        return Response("Ushbu oy uchun allaqachon to'lov qilingan.", status=status.HTTP_400_BAD_REQUEST)

    if month:
        try:
            models.Subscription.objects.create(
                cost=amount,
                month=datetime(int(current_year), int(month), 1),
                group=group,
                student=student,
                company=company,
                status='1'
            )
        except:
            return Response("Parametrlar xato berilgan", status=status.HTTP_400_BAD_REQUEST)
    else:
        models.Subscription.objects.create(
            cost=amount,
            group=group,
            student=student,
            company=company,
            status='1'
        )

    return Response("To'lov muvaffaqiyatli kiritildi", status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.ProfileLevelPermission])
def delete_student(request, pk):

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    try:
        student = models.Student.objects.get(
            id=pk, company=company, status='1')
    except:
        return Response("O'quvchi topilmadi", status=status.HTTP_400_BAD_REQUEST)

    student.status = '0'
    student.save()

    return Response("O'quvchi o'chirildi", status=status.HTTP_204_NO_CONTENT)
