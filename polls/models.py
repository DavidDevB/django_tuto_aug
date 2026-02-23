from django.db import models


class Question(models.Model):
    question_text: models.CharField = models.CharField(max_length=200)
    pub_date: models.DateTimeField = models.DateTimeField("date published")


class Choice(models.Model):
    question: models.ForeignKey = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text: models.CharField = models.CharField(max_length=200)
    votes: models.IntegerField = models.IntegerField(default=0)