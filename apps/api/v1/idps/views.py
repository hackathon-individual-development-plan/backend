from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.api.v1.idps.mixinview import CreateRetrieveViewSet, CreateViewSet
from apps.api.v1.idps.serializers import (
    IdpSerializer,
    PostCommentSerializer,
    PostIdpSerializer,
    PutIdpSerializer,
)
from apps.idps.models import Comment, Goal, Idp


class IdpViewSet(CreateRetrieveViewSet):
    """Вьюсет для просмотра ИПР, создания и редактирования."""

    # permission_classes = (IsChief,) TODO написать пермишн
    ordering_fields = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostIdpSerializer
        if self.request.method == "PUT":
            return PutIdpSerializer
        return IdpSerializer

    def get_queryset(self):
        queryset = Idp.objects.all().prefetch_related(
            Prefetch(
                "idp_goals",
                queryset=Goal.objects.prefetch_related("goals_tasks"),
            )
        )
        return queryset

    def create(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, id=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CommentViewSet(CreateViewSet):
    """Вьюсет для просмотра и создания комментариев."""

    # permission_classes=[IsAuthenticated]
    serializer_class = PostCommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        goal = get_object_or_404(Goal, id=self.kwargs.get("goal_id"))
        author_comment = self.request.user
        serializer.save(
            goal=goal,
            user=author_comment,
        )
