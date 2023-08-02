from rest_framework import permissions
from .models import Profile



class AllLevelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return False
        
        return (profile.level == 'admin' or profile.level == 'casher' or profile.level == 'teacher') and request.user.is_authenticated and profile.is_active

class ProfileLevelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return False
        
        return (profile.level == 'admin' or profile.level == 'casher') and request.user.is_authenticated and profile.is_active
    

        
class TeacherLevelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return False

        return profile.level == 'teacher' and request.user.is_authenticated and profile.is_active
    


class AdminLevelPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            try:
                profile = Profile.objects.get(user=request.user)
            except:
                return False

            return profile.level == 'admin' and request.user.is_authenticated and profile.is_active



class ManagerLevelPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            try:
                profile = Profile.objects.get(user=request.user)
            except:
                return False

            return profile.level == 'null' and request.user.is_authenticated



class OwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            # Allow read-only permissions (GET, HEAD, OPTIONS) for all users.
            if request.method in permissions.SAFE_METHODS:
                return True
            
            try:
                profile = Profile.objects.get(user=request.user)
            except:
                return False

            # Check if the user making the request is the author of the post.
            return obj.company == profile.company