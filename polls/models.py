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
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1) and self.pub_date <= timezone.now()
    
    @property
    def total_votes(self):
        return self.choice_set.aggregate(models.Sum("votes"))["votes__sum"] or 0
    
    @property
    def average_votes_per_question(self):
        total_questions = Question.objects.count()
        if total_questions > 0:
            return self.total_votes / total_questions
        else:
            return 0
        
    @property
    def total_choices(self):
        return self.choice_set.count()
    
    @property
    def most_popular_question(self):
        return Question.objects.annotate(votes_sum=models.Sum("choice__votes")).order_by("-votes_sum").first()
    
    @property
    def less_popular_question(self):
        return Question.objects.annotate(votes_sum=models.Sum("choice__votes")).order_by("votes_sum").first()
    
    @property
    def last_registered_question(self):
        return Question.objects.order_by("-pub_date").first()

class Choice(models.Model):
    question: models.ForeignKey = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text: models.CharField = models.CharField(max_length=200)
    votes: models.IntegerField = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
    def get_percentage(self):
        total_votes = self.question.choice_set.aggregate(models.Sum("votes"))["votes__sum"] or 0
        if total_votes > 0:
            return (self.votes / total_votes) * 100
        else:
            return 0
    

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