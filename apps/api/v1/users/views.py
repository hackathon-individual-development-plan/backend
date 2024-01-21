from django.db.models import Prefetch
from rest_framework import viewsets

from apps.idps.models import Idp
from apps.users.models import ChiefEmployee

from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     queryset = ChiefEmployee.objects.filter(chief=1).prefetch_related(
    #         Prefetch("employee__my_idp", queryset=Idp.objects.all()))
    #     return queryset

    serializer_class = EmployeeSerializer
    queryset = ChiefEmployee.objects.filter(chief=1).prefetch_related(
        Prefetch("employee__my_idp", queryset=Idp.objects.all())
    )
