from rest_framework import viewsets

from apps.api.v1.idps.serializers import IdpSerializer, PostIdpSerializer
from apps.idps.models import Idp


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    # permission_classes = (IsChief,) TODO написать пермишн
    ordering_fields = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return PostIdpSerializer
        return IdpSerializer


# class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Ingredient.objects.all()
#     pagination_class = None
#     serializer_class = IngredientsSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = IngredientsFilter
