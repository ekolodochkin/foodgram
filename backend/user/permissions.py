from rest_framework import permissions


class ForAuthUserOrAllowAny(permissions.IsAuthenticated):
    """ -- для юзера user.views -- """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.method == 'POST')

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated