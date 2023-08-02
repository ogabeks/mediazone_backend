from rest_framework.routers import SimpleRouter
from api import views


urlpatterns = []

router = SimpleRouter()

router.register('profiles', views.ProfileViewset)
router.register('settings', views.CompanySettingsViewset)
router.register('company', views.CompanyViewset)
router.register('subscription', views.CompanySubsciptionViewset)
router.register('subjects', views.SubjectViewset)
router.register('students', views.StudentViewset)
router.register('groups', views.GroupViewset)
router.register('payment', views.SubscriptionViewset)
router.register('teacher/bonus', views.TeacherBonusViewset)
router.register('teacher/attendace', views.TeacherAttendaceViewset)
router.register('teacher/fine', views.TeacherFinesViewset)
router.register('teacher/debt', views.TeacherDebtsViewset)
router.register('expenses', views.ExpensesViewset)



urlpatterns += router.urls