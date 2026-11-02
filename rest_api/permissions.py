from rest_framework.permissions import IsAuthenticated

class IsUserNameDjango2(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        user = request.user
        return user.username.lower() != 'django2'