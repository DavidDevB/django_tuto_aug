from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.db import models
from django.utils import timezone


from .models import Question, Choice
from .forms import ContactForm
from django.core.mail import send_mail

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :10
    ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return all published questions."""
        return Question.objects.order_by("-pub_date")


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

    def post(self, request):

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


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["info@example.com"]
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, "name.html", {"form": form})