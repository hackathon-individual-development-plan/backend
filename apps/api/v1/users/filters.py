from django_filters.rest_framework import CharFilter, FilterSet

from apps.users.models import ChiefEmployee


class EmployeeWithoutIdpFilter(FilterSet):
    """Поиск по частичному вхождению в начале ФИО."""

    fio = CharFilter(field_name="employee__fio", lookup_expr="istartswith")

    class Meta:
        model = ChiefEmployee
        fields = ["fio"]
