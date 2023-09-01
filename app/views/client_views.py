from app.models import CompanySettings
import requests
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from app import models, permissions, serializers
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.models import User
from django.db import transaction

current_day = timezone.now().day
current_month = timezone.now().month
current_year = timezone.now().year


def send_msg(company, reciever, text, msg_type):
    settings = CompanySettings.objects.get(company=company)

    is_true = False
    # url = 'http://91.204.239.42:8083/broker-api/send'
    if msg_type == 'mark':
        if settings.mark:
            is_true = True
    if msg_type == 'payment':
        if settings.payment:
            is_true = True
    if msg_type == 'attendace':
        if settings.attendace:
            is_true = True

    if is_true:

        url = settings.api_link

        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Accept': 'text/plain',
                   'Authorization': f'Basic {settings.key}'}
        data = {
            "messages":
            [
                {
                    "recipient": reciever,
                    "message-id": "3700",

                    "sms": {

                        "originator": settings.originator,
                        "content": {
                            "text": text
                        }
                    }
                }
            ]
        }
        response = requests.post(url, json=data, headers=headers)
        return response.status_code


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
class StudentViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Pop the 'students' data from request.data for special handling
        students_data = request.data.pop('students', None)

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated instance without 'students'
        self.perform_update(serializer)

        # Handle 'students' data separately if provided
        if students_data is not None:
            instance.students.set([])  # Clear existing students
            for student_data in students_data:
                student_instance, created = models.Student.objects.get_or_create(
                    student_id=student_data['student_id'],
                    defaults=student_data
                )
                if not created:
                    serializers.StudentSerializer(
                        instance=student_instance, data=student_data, partial=True
                    ).is_valid(raise_exception=True)
                    student_instance.save()
                instance.students.add(student_instance)

        return Response(serializer.data)

# TEACHERS VIEWSET


class TeacherViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.AllLevelPermission,
                          permissions.OwnerPermission]
    queryset = models.Profile.objects.all().order_by('-id')
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(
                company=company, level='teacher', is_active=True)
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
        date = self.request.query_params.get('date', None)

        user = self.request.user

        # try:

        company = models.Profile.objects.get(user=user).company
        if date:
            cyear = date.split("-")[0]
            cmonth = date.split('-')[1]
            cday = date.split("-")[2]
            queryset = queryset.filter(company=company, created_at__year=int(
                cyear), created_at__month=int(cmonth), created_at__day=int(cday))
        else:
            queryset = queryset.filter(
                company=company, created_at__day=current_day, created_at__month=current_month, created_at__year=current_year)

        print(len(queryset))

        # except:
        #     return None

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
        month = self.request.query_params.get('month', None)
        queryset = super().get_queryset()
        user = self.request.user

        try:
            company = models.Profile.objects.get(user=user).company
            queryset = queryset.filter(company=company)

            if month:
                month = int(month)
                queryset = queryset.filter(
                    date__month=month, date__year=current_year)
            else:
                queryset = queryset.filter(
                    date__month=current_month, date__year=current_year)
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

    company_settings = models.CompanySettings.objects.get(company=company)
    c_date = f'{timezone.now().year}-{timezone.now().month}-{timezone.now().day}  {timezone.now().hour}:{timezone.now().minute}'
    if company_settings.payment and student.sms_service:
        text = f'{company.name}\nTo`lov amalga oshirildi.\nTalaba: {student.name}\nSumma: {amount}\nFan: {group.subject.name}\n Sana: {c_date}'

        send_msg(company=company, reciever=student.phone,
                 text=text, msg_type='payment')

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


@api_view(['GET'])
@permission_classes([permissions.ProfileLevelPermission])
def subscription_history(request, pk):

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

    history = models.Subscription.objects.filter(
        student__id=student.pk, company__id=company.pk).order_by('month')

    data = serializers.SubscriptionSerializer(history, many=True).data

    return Response({"data": data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.ProfileLevelPermission])
def data_stats(request):

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    all_subscriptions = 0
    groups = models.Group.objects.filter(company=company, status='1')
    subscriptions = models.Subscription.objects.filter(
        company=company, status='1', month__month=current_month, month__year=current_year, group__status='1')

    s_count = 0

    for group in groups:
        s = models.Subscription.objects.filter(
            group=group, company=company, status='1', month__month=current_month, month__year=current_year)
        s_count += s.count()
        all_subscriptions += group.students.count()

    print(all_subscriptions, subscriptions.count())

    unpayment = all_subscriptions - s_count
    print(unpayment, groups.count())

    groups_serializer = serializers.GroupSerializer(groups, many=True).data

    return Response({"unpayment": unpayment, 'groups_count': groups.count(), 'groups': groups_serializer}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.ProfileLevelPermission])
def delete_group(request, pk):

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    try:
        group = models.Group.objects.get(id=pk, company=company)
    except:
        return Response("Guruh topilmadi", status=status.HTTP_400_BAD_REQUEST)

    for student in group.students.all():
        group.students.remove(student)

    group.status = '0'
    group.save()

    return Response("Guruh o'chirildi", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.ProfileLevelPermission])
def teacher_stats(request, pk):
    print("good")

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    try:
        teacher = models.Profile.objects.get(
            id=pk, company=company, level='teacher')
    except:
        return Response("O'qituvchi topilmadi", status=status.HTTP_400_BAD_REQUEST)

    teacher_bonuses = serializers.TeacherBonusSerializer(models.TeacherBonus.objects.filter(
        teacher=teacher, date__year=current_year, date__month=current_month), many=True).data

    teacher_fines = serializers.TeacherFineSerializer(models.TeacherFine.objects.filter(
        teacher=teacher, date__year=current_year, date__month=current_month), many=True).data

    teacher_debts = serializers.TeacherDebtSerializer(models.TeacherDebt.objects.filter(
        teacher=teacher, date__year=current_year, date__month=current_month), many=True).data

    teacher_attendace = serializers.TeacherAttendaceSerializer(models.TeacherAttendace.objects.filter(
        teacher=teacher, date__year=current_year, date__month=current_month), many=True).data

    response = {
        'bonuses': teacher_bonuses,
        'fines': teacher_fines,
        'debts': teacher_debts,
        'attendace': teacher_attendace
    }

    return Response(response, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.ProfileLevelPermission])
def delete_teacher(request, pk):

    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    try:
        teacher = models.Profile.objects.get(
            id=pk, company=company, level='teacher')
    except:
        return Response("O'qituvchi topilmadi", status=status.HTTP_400_BAD_REQUEST)

    teacher.is_active = False
    teacher.save()

    return Response("O'qituvchi o'chirildi", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.ProfileLevelPermission])
def create_teacher(request):
    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    data = request.data

    user = User.objects.create_user(username=data.get(
        'username'), password=data.get('password'))
    profile = models.Profile.objects.create(name=data.get('name'), user=user, phone=data.get(
        'username'), level='teacher', company=company, is_active=True)

    return Response("O'qituvchi kiritildi", status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([permissions.ProfileLevelPermission])
def edit_teacher(request, pk):
    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    data = request.data

    profile = models.Profile.objects.get(id=pk, company=company)
    user = profile.user
    with transaction.atomic():
        user.username = data.get('phone')
        user.save()
        profile.name = data.get('name')
        profile.phone = data.get('phone')
        profile.save()
        return Response("O'qituvchi malumotlari yangilandi", status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([permissions.ProfileLevelPermission])
def edit_user(request):
    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    data = request.data

    profile = models.Profile.objects.get(user=request.user, company=company)
    user = profile.user
    with transaction.atomic():
        user.username = data.get('phone')
        user.save()
        profile.name = data.get('name')
        profile.phone = data.get('phone')
        profile.save()
        return Response("Profil malumotlari yangilandi", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.ProfileLevelPermission])
def get_company(request):
    try:
        company = models.Profile.objects.get(
            user=request.user, is_active=True).company
    except:
        return Response("Ruxsat berilmagan", status=status.HTTP_400_BAD_REQUEST)

    data = request.data

    try:
        company_settings = models.CompanySettings.objects.get(company=company)
    except:
        company_settings = models.CompanySettings.objects.create(
            company=company)

    company_data = serializers.CompanySerializer(
        models.Company.objects.get(id=company.pk)).data

    settings_data = serializers.CompanySettingsSerializer(
        company_settings).data

    return Response({'company': company_data, 'settings': settings_data}, status=status.HTTP_200_OK)
