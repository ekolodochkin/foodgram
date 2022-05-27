from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscribeView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path(
        'users/<int:user_id>/subscribe/',
        SubscribeView.as_view(),
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
