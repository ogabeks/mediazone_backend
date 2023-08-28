from rest_framework.routers import SimpleRouter
from app import views
from django.urls import path


urlpatterns = []

router = SimpleRouter()

router.register('profiles', views.ProfileViewset)
router.register('settings', views.CompanySettingsViewset)
router.register('company', views.CompanyViewset)
router.register('subscription', views.CompanySubsciptionViewset)
router.register('subjects', views.SubjectViewset)
router.register('students', views.StudentViewset)
router.register('teachers', views.TeacherViewset)
router.register('groups', views.GroupViewset)
router.register('payment', views.SubscriptionViewset)
router.register('teacher/bonus', views.TeacherBonusViewset)
router.register('teacher/attendace', views.TeacherAttendaceViewset)
router.register('teacher/fine', views.TeacherFinesViewset)
router.register('teacher/debt', views.TeacherDebtsViewset)
router.register('expenses', views.ExpensesViewset)

urlpatterns = [
    path('check-student/', views.check_student),
    path('is_subscribed/', views.is_subscribed),
    path('add_subscription/', views.add_subscription),
    path('actions/students/<int:pk>/', views.delete_student),
    path('actions/students/<int:pk>/subscription_history/',
         views.subscription_history),

    path('data_stats/', views.data_stats),
    path('actions/group/<int:pk>/delete/', views.delete_group),
    path('actions/teachers/<int:pk>/delete/', views.delete_teacher),
    path('actions/teachers/<int:pk>/edit/', views.edit_teacher),

    path('actions/teachers/insert/', views.create_teacher),

    path('teachers/<int:pk>/stats/', views.teacher_stats)

]


urlpatterns += router.urls
