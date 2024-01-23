from rest_framework import serializers

from apps.idps.models import Idp
from apps.users.models import ChiefEmployee, User


class IdpForEmployeesSerializer(serializers.ModelSerializer):
    """Сериализация данных об ИПР.

    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = Idp
        fields = ["id", "title", "status"]


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике: ФИО и должность.

    Используется в сериализаторе EmployeeSerializer.
    """

    class Meta:
        model = User
        fields = ["id", "fio", "job_title"]


class UserFIOSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотруднике: ФИО.

    Используется в сериализаторе EmployeeWithoutIdpSerializer.
    """

    class Meta:
        model = User
        fields = ["fio"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализация данных о сотрудниках и их ИПР."""

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
