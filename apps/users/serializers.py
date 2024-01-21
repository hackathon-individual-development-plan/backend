from models import ChiefEmployee, User, UserRole
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "fio", "job_title"]


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["id", "user", "role"]


class ChiefEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiefEmployee
        fields = ["id", "chief", "employee"]
