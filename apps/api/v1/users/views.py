from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.response import Response

from apps.idps.models import Idp, Status
from apps.users.models import ChiefEmployee

from .serializers import EmployeeSerializer, EmployeeWithoutIdpSerializer


class EmployeeViewSet(viewsets.GenericViewSet):
    serializer_class = EmployeeSerializer

    # TODO: ЗАГЛУШКА
    # после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     return ChiefEmployee.objects.filter(chief=chief).prefetch_related(
    #         Prefetch("employee__my_idp", queryset=Idp.objects.all()))

    queryset = ChiefEmployee.objects.filter(chief=1).prefetch_related(
        Prefetch("employee__my_idp", queryset=Idp.objects.all())
    )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeWithoutIdpViewSet(viewsets.GenericViewSet):
    serializer_class = EmployeeWithoutIdpSerializer

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
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
