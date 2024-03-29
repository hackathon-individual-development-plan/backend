from rest_framework import serializers

from apps.users.models import ChiefEmployee

from ...idps.serializers import IdpForEmployeesSerializer, MyIdpSerializer
from .users import UserFIOSerializer, UserSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотрудниках и их ИПР (id, название, статус)."""

    employee = UserSerializer()
    idp = IdpForEmployeesSerializer(
        source="employee.my_idp", many=True, read_only=True
    )

    class Meta:
        model = ChiefEmployee
        fields = ["employee", "idp"]


class EmployeeWithoutIdpSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотрудниках, у которых нет ИПР в работе."""

    employee = UserFIOSerializer()

    class Meta:
        model = ChiefEmployee
        fields = ["employee"]


class EmployeeMyIdpSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике и его ИПР (id, название, статус, цели и задачи)."""

    employee = UserSerializer()
    idp = MyIdpSerializer(source="employee.my_idp", many=True, read_only=True)

    class Meta:
        model = ChiefEmployee
        fields = ["employee", "idp"]
