from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.api.v1.idps.mixinview import CreateRetrieveViewSet, CreateViewSet
from apps.api.v1.idps.serializers import (  # PatchIdpSerializer,
    GoalForIdp,
    IdpSerializer,
    PostCommentSerializer,
    PostIdpSerializer,
    PUTIdpSerializer,
)
from apps.idps.models import Comment, Idp

# , Task


class IdpViewSet(CreateRetrieveViewSet):
    queryset = Idp.objects.all().prefetch_related(
        Prefetch(
            "idp_goals",
            queryset=GoalForIdp.objects.prefetch_related("goals_tasks"),
        )
    )
    #   queryset = Idp.objects.all().prefetch_related(
    #       Prefetch(
    #           "idp_goals",
    #           queryset=GoalForIdp.objects.prefetch_related(
    #                   "goals_tasks",
    #           ),
    #       )
    #   )

    def retrieve(self, request, pk=None):
        queryset = Idp.objects.filter(id=pk).prefetch_related(
            Prefetch(
                "idp_goals",
                queryset=GoalForIdp.objects.prefetch_related(
                    "goals_tasks",
                ),
            )
        )
        serializer = IdpSerializer(queryset[0])
        return Response(serializer.data)

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
            return PUTIdpSerializer
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
