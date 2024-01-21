from rest_framework import viewsets

from apps.api.v1.idps.serializers import IdpForEmployeesSerializer
from apps.idps.models import Idp


class IdpForEmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = IdpForEmployeesSerializer
    queryset = Idp.objects.all()
