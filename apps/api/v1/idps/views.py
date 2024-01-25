from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from apps.api.v1.idps.mixinview import CreateRetrieveViewSet, CreateViewSet
from apps.api.v1.idps.serializers import (
    GoalForIdp,
    IdpSerializer,
    PostCommentSerializer,
    PostIdpSerializer,
    PutIdpSerializer,
)
from apps.idps.models import Comment, Idp


class IdpViewSet(CreateRetrieveViewSet):
    queryset = Idp.objects.all().prefetch_related(
        Prefetch(
            "goals",
            queryset=GoalForIdp.objects.prefetch_related("goal_comment"),
        )
    )
    # permission_classes = (IsChief,) TODO написать пермишн
    ordering_fields = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method in [
            "POST",
        ]:
            return PostIdpSerializer
        if self.request.method in [
            "PUT",
        ]:
            return PutIdpSerializer
        return IdpSerializer


class CommentViewSet(CreateViewSet):
    # permission_classes=[IsAuthenticated]
    serializer_class = PostCommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        goal = get_object_or_404(GoalForIdp, id=self.kwargs.get("goal_id"))
        author_comment = self.request.user
        serializer.save(
            goal=goal,
            user=author_comment,
        )
