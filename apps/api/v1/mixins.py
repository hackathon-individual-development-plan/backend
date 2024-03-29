from rest_framework import mixins, viewsets


class CreateRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
