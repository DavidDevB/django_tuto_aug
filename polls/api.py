from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Choice, Question
from .serializers import ChoiceSerializer, QuestionSerializer, VoteSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related("choice_set").order_by("-pub_date")
    serializer_class = QuestionSerializer

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.AllowAny],
        serializer_class=VoteSerializer,
    )
    def vote(self, request, pk=None):
        """POST /api/questions/<id>/vote/ avec {"choice": <id du choix>}"""
        question = self.get_object()
        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        choice = get_object_or_404(
            question.choice_set, pk=serializer.validated_data["choice"]
        )
        choice.votes = F("votes") + 1
        choice.save()
        choice.refresh_from_db()
        return Response(ChoiceSerializer(choice).data)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.select_related("question").order_by("id")
    serializer_class = ChoiceSerializer
