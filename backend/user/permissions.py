from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class AllowAnyGetPost(IsAuthenticated):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.method == 'POST')


class CurrentUserOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return request.user.is_superuser or obj.pk == user.pk