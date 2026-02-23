import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text: models.CharField = models.CharField(max_length=200)
    pub_date: models.DateTimeField = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question: models.ForeignKey = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text: models.CharField = models.CharField(max_length=200)
    votes: models.IntegerField = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    ordering = ["pub_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "choice_text", "votes")
    list_filter = ["question"]
    ordering = ["question", "votes"]
    search_fields = ["choice_text"]