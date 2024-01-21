from django.db.models import Prefetch
from rest_framework import viewsets

from apps.idps.models import Idp, Status
from apps.users.models import ChiefEmployee

from .serializers import EmployeeSerializer, EmployeeWithoutIdpSerializer


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmployeeSerializer

    # TODO: ЗАГЛУШКА
    # после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     queryset = ChiefEmployee.objects.filter(chief=chief).prefetch_related(
    #         Prefetch("employee__my_idp", queryset=Idp.objects.all()))
    #     return queryset
    queryset = ChiefEmployee.objects.filter(chief=1).prefetch_related(
        Prefetch("employee__my_idp", queryset=Idp.objects.all())
    )


class EmployeeWithoutIdpViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmployeeWithoutIdpSerializer

    # TODO: ЗАГЛУШКА
    # после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     employees_with_idp = Idp.objects.filter(status=Status.IN_PROGRESS).values_list('employee', flat=True)
    #     queryset = ChiefEmployee.objects.filter(chief=chief).exclude(employee__in=employees_with_idp)
    #     return queryset
    employees_with_idp = Idp.objects.filter(
        status=Status.IN_PROGRESS
    ).values_list("employee", flat=True)
    queryset = ChiefEmployee.objects.filter(chief=1).exclude(
        employee__in=employees_with_idp
    )
