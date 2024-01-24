from django.db.models import OuterRef

from apps.api.v1.idps.mixinview import CreateRetrieveViewSet
from apps.api.v1.idps.serializers import IdpSerializer, PostIdpSerializer
from apps.idps.models import GoalTask, Idp


class IdpViewSet(CreateRetrieveViewSet):
    tasks_for_goal = GoalTask.objects.filter(goal_id=OuterRef("goal_id"))
    queryset = Idp.objects.all().prefetch_related("goals")
    # permission_classes = (IsChief,) TODO написать пермишн
    ordering_fields = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return PostIdpSerializer
        return IdpSerializer
