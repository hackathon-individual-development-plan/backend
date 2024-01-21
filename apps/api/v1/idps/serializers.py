from rest_framework import serializers

from apps.idps.models import Idp


class IdpForEmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        fields = ["title", "status"]
