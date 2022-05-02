from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', )


urlpatterns = [
    path('', include(router.urls)),
]

# Юзер (get post)
# http://localhost/api/users/{id}/
# Djoser
# http://localhost/api/users/
# http://localhost/api/users/me/
# http://localhost/api/users/set_password/
# http://localhost/api/auth/token/login/
# http://localhost/api/auth/token/logout/

# Подписки (get, post, del)
# http://localhost/api/users/subscriptions/
# http://localhost/api/users/{id}/subscribe/
#