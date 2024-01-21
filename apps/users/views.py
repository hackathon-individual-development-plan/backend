from models import ChiefEmployee, User, UserRole
from rest_framework import viewsets
from serializers import ChiefEmployeeSerializer, UserRoleSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer


class ChiefEmployeeViewSet(viewsets.ModelViewSet):
    queryset = ChiefEmployee.objects.all()
    serializer_class = ChiefEmployeeSerializer
