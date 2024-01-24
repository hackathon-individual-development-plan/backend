from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    EmployeeIdpViewSet,
    EmployeeViewSet,
    EmployeeWithoutIdpViewSet,
    IdpViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()


router_v1.register("employees", EmployeeViewSet, basename="employees")
router_v1.register(
    "employees-without-idp",
    EmployeeWithoutIdpViewSet,
    basename="employees-without-idp",
)
router_v1.register("employee", EmployeeIdpViewSet, basename="employee")
router_v1.register("idps", IdpViewSet, basename="idps")


urlpatterns = [path("", include(router_v1.urls))]
