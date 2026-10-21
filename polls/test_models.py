import datetime
import pytest
from django.utils import timezone
from polls.models import Question, Choice
from django.db import models


    #Fixture
@pytest.fixture
def question():
    return Question(question_text="What is your favorite dish?", pub_date=timezone.now())

@pytest.fixture
def total_votes():
    return Choice.objects.aggregate(models.Sum("votes"))["votes__sum"]

def test_str_method():
    question = Question(question_text="What is your favorite dish?", pub_date=timezone.now())
    assert str(question) == "What is your favorite dish?"

def test_repr_method():
    question = Question(question_text="What is your favorite dish?", pub_date=timezone.now())
    assert repr(question) == "<Question: What is your favorite dish?>"

def test_was_published_recently_with_future_question():
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    assert future_question.was_published_recently() is False

