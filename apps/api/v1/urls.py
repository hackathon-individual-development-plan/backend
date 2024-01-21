from django.urls import include, path
from rest_framework import routers

from .users.views import EmployeeViewSet, EmployeeWithoutIdpViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employees")
router.register(
    "employees-without-idp",
    EmployeeWithoutIdpViewSet,
    basename="employees-without-idp",
)

urlpatterns = [path("", include(router.urls))]
