from django.db.models import OuterRef, Prefetch, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.idps.models import Idp, Status
from apps.users.models import ChiefEmployee

from ..mixins import ListViewSet
from ..permissions import IsChief, ReadOnly
from .filters import EmployeeWithoutIdpFilter
from .serializers.employees import (
    EmployeeMyIdpSerializer,
    EmployeeSerializer,
    EmployeeWithoutIdpSerializer,
)
from .serializers.users import UserInfoSerializer


class UserInfoViewSet(viewsets.GenericViewSet):
    """Вьюсет используется для получения информации, включая роль, о
    текущем пользователе.
    """

    serializer_class = UserInfoSerializer

    @action(methods=["get"], detail=False, url_path="current-user")
    def current_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class EmployeeViewSet(ListViewSet):
    """Вьюсет используется для получения списка всех сотрудников
    текущего пользователя - руководителя -
    и информации об их ИПР (айди, название, статус).
    """

    permission_classes = (IsChief,)
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        chief = self.request.user
        latest_idp = (
            Idp.objects.filter(employee_id=OuterRef("employee_id"))
            .order_by("-created_at")
            .values("id")[:1]
        )
        return ChiefEmployee.objects.filter(chief=chief).prefetch_related(
            Prefetch(
                "employee__my_idp",
                queryset=Idp.objects.filter(id__in=Subquery(latest_idp)),
            )
        )


class EmployeeWithoutIdpViewSet(ListViewSet):
    """Вьюсет используется для получения списка сотрудников
    текущего пользователя - руководителя, -
    у которых отсутствует ИПР в статусе В работе.
    """

    permission_classes = (IsChief,)
    serializer_class = EmployeeWithoutIdpSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = EmployeeWithoutIdpFilter

    def get_queryset(self):
        chief = self.request.user
        employees_with_idp = Idp.objects.filter(
            status=Status.IN_PROGRESS
        ).values_list("employee", flat=True)
        return ChiefEmployee.objects.filter(chief=chief).exclude(
            employee__in=employees_with_idp
        )


class EmployeeIdpViewSet(ListViewSet):
    """Вьюсет используется для получения данных о последнем ИПР
    (Мой ИПР) текущего пользователя - сотрудника.
    """

    permission_classes = (ReadOnly,)

    serializer_class = EmployeeMyIdpSerializer

    def get_queryset(self):
        employee = self.request.user
        latest_idp = (
            Idp.objects.filter(employee_id=OuterRef("employee_id"))
            .order_by("-created_at")
            .values("id")[:1]
        )
        return ChiefEmployee.objects.filter(
            employee=employee
        ).prefetch_related(
            Prefetch(
                "employee__my_idp",
                queryset=Idp.objects.filter(id__in=Subquery(latest_idp)),
            )
        )
