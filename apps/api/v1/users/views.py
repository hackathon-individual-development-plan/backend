from django.db.models import OuterRef, Prefetch, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from apps.idps.models import Idp, Status
from apps.users.models import ChiefEmployee

from .filters import EmployeeWithoutIdpFilter
from .permissions import IsOwnerOrReadOnly, ReadOnly
from .serializers.employees import (
    EmployeeSerializer,
    EmployeeWithoutIdpSerializer,
)


class EmployeeViewSet(viewsets.GenericViewSet):
    """Вьюсет используется для получения списка сотрудников
    текущего пользователя - руководителя -
    и информации об их ИПР (айди, название, статус).
    """

    serializer_class = EmployeeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    latest_idp = (
        Idp.objects.filter(employee_id=OuterRef("employee_id"))
        .order_by("-created_at")
        .values("id")[:1]
    )

    # TODO: ЗАГЛУШКА
    # после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     return ChiefEmployee.objects.filter(chief=chief).prefetch_related(
    #         Prefetch("employee__my_idp",
    #                  queryset=Idp.objects.filter(id__in=Subquery(latest_idp)))

    queryset = ChiefEmployee.objects.filter(chief=1).prefetch_related(
        Prefetch(
            "employee__my_idp",
            queryset=Idp.objects.filter(id__in=Subquery(latest_idp)),
        )
    )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeWithoutIdpViewSet(viewsets.GenericViewSet):
    """Вьюсет используется для получения списка сотрудников
    текущего пользователя - руководителя, -
    у которых отсутствует ИПР в статусе В работе.
    """

    serializer_class = EmployeeWithoutIdpSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = EmployeeWithoutIdpFilter
    permission_classes = (IsOwnerOrReadOnly,)

    employees_with_idp = Idp.objects.filter(
        status=Status.IN_PROGRESS
    ).values_list("employee", flat=True)

    # TODO: ЗАГЛУШКА
    # после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     return ChiefEmployee.objects.filter(chief=chief).exclude(
    #         employee__in=employees_with_idp)

    queryset = ChiefEmployee.objects.filter(chief=1).exclude(
        employee__in=employees_with_idp
    )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeIdpViewSet(viewsets.GenericViewSet):
    """Вьюсет используется для получения данных о последнем ИПР
    (Мой ИПР) текущего пользователя - сотрудника.
    """

    # TODO: ЗАГЛУШКА
    # после мержа ИПР сериализатора
    # заменить на serializer_class = EmployeeMyIdpSerializer
    serializer_class = EmployeeSerializer
    permission_classes = (ReadOnly,)

    latest_idp = (
        Idp.objects.filter(employee_id=OuterRef("employee_id"))
        .order_by("-created_at")
        .values("id")[:1]
    )

    # TODO: ЗАГЛУШКА
    # после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     employee = self.request.user
    #     return ChiefEmployee.objects.filter(employee=employee).prefetch_related(
    #         Prefetch("employee__my_idp",
    #                  queryset=Idp.objects.filter(id__in=Subquery(latest_idp)))

    queryset = ChiefEmployee.objects.filter(employee=2).prefetch_related(
        Prefetch(
            "employee__my_idp",
            queryset=Idp.objects.filter(id__in=Subquery(latest_idp)),
        )
    )

    @action(detail=False, methods=["get"], url_path="my-idp")
    def get_my_idp(self, request):
        instance = self.queryset.get()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
