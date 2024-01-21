from rest_framework import viewsets

from apps.api.v1.users.serializers import (
    ChiefEmployeeSerializer,
    EmployeeSerializer,
    UserRoleSerializer,
    UserSerializer,
)
from apps.users.models import ChiefEmployee, User, UserRole


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer


class ChiefEmployeeViewSet(viewsets.ModelViewSet):
    queryset = ChiefEmployee.objects.all()
    serializer_class = ChiefEmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    # TODO: после реализации авторизации взять юзера из request (self.request.user)
    # def get_queryset(self):
    #     chief = self.request.user
    #     employees = ChiefEmployee.objects.filter(chief=chief).select_related("employee")
    #     return employees

    serializer_class = EmployeeSerializer
    queryset = ChiefEmployee.objects.filter(chief_id=1).select_related("employee")
