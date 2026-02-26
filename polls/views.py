from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.db import models
from django import forms


from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("-pub_date")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
class FrequencyView(generic.DetailView):
    model = Question
    template_name = "polls/frequency.html"

class StatisticsView(generic.ListView):
    template_name = "polls/statistics.html"
    context_object_name = "questions"

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("-pub_date")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_questions'] = Question.objects.count()
        context['total_votes'] = Choice.objects.aggregate(
            total=models.Sum("votes")
        )["total"] or 0
        context['total_choices'] = Choice.objects.count()
        context['most_popular'] = Question.objects.annotate(votes_sum=models.Sum("choice__votes")).order_by("-votes_sum").first()
        return context

class QuestionFormView(View):
    model = Question
    template_name = "polls/form.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        question_text = request.POST.get("question_text", "")
        choice1_text = request.POST.get("choice1", "")
        choice2_text = request.POST.get("choice2", "")
        choice3_text = request.POST.get("choice3", "")
        choice4_text = request.POST.get("choice4", "")
        choice5_text = request.POST.get("choice5", "")
        pub_date = request.POST.get("pub_date", "")

        question = Question.objects.create(question_text=question_text, pub_date=pub_date)
        
        for choice_text in [choice1_text, choice2_text, choice3_text, choice4_text, choice5_text]:
            if choice_text:
                Choice.objects.create(question=question, choice_text=choice_text)
        
        return HttpResponseRedirect(reverse("polls:results", args=(question.pk,)))


