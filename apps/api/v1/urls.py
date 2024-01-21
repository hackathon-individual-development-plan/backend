from django.urls import include, path
from rest_framework import routers

from apps.api.v1.users.views import EmployeeViewSet, UserViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("employees", EmployeeViewSet, basename="employees")

urlpatterns = [path("", include(router.urls))]
