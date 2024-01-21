from rest_framework import viewsets

from apps.idps.models import Idp

from .serializers import IdpForEmployeesSerializer


class IdpForEmployeesViewSet(viewsets.ModelViewSet):
    serializer_class = IdpForEmployeesSerializer
    queryset = Idp.objects.all()
