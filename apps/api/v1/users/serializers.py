from rest_framework import serializers

from apps.users.models import ChiefEmployee, User

from ..idps.serializers import IdpForEmployeesSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fio", "job_title"]


class UserFIOSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fio"]


class EmployeeSerializer(serializers.ModelSerializer):
    employee = UserSerializer()
    idp = IdpForEmployeesSerializer(
        source="employee.my_idp", many=True, read_only=True
    )

    class Meta:
        model = ChiefEmployee
        fields = ["employee", "idp"]


class EmployeeWithoutIdpSerializer(serializers.ModelSerializer):
    employee = UserFIOSerializer()

    class Meta:
        model = ChiefEmployee
        fields = ["employee"]
