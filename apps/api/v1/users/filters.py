from django_filters.rest_framework import CharFilter, FilterSet

from apps.users.models import User


class EmployeeWithoutIdpFilter(FilterSet):
    """Поиск по частичному вхождению в начале ФИО."""

    name = CharFilter(lookup_expr="istartswith")

    class Meta:
        model = User
        fields = [
            "fio",
        ]
