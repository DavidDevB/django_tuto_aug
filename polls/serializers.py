from rest_framework import serializers

from .models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "question", "choice_text", "votes"]
        read_only_fields = ["votes"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True, read_only=True)
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "total_votes", "choices"]


class VoteSerializer(serializers.Serializer):
    choice = serializers.IntegerField()
