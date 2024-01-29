from django.urls import include, path
from rest_framework import routers

from .idps.views import CommentViewSet, IdpViewSet
from .users.views import (
    EmployeeIdpViewSet,
    EmployeeViewSet,
    EmployeeWithoutIdpViewSet,
    UserInfoViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register("user-info", UserInfoViewSet, basename="user-info")
router.register("employees", EmployeeViewSet, basename="employees")
router.register(
    "employees-without-idp",
    EmployeeWithoutIdpViewSet,
    basename="employees-without-idp",
)
router.register(
    "employee",
    EmployeeIdpViewSet,
    basename="employee",
)
router.register(
    r"idps/(?P<idp_id>\d+)/goals/(?P<goal_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register("idps", IdpViewSet, basename="idps")

urlpatterns = [path("", include(router.urls))]
