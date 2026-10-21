import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
from rest_framework.test import APIClient

from polls.models import Choice, Question


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def question():
    question = Question.objects.create(question_text="What's up?", pub_date=timezone.now())
    Choice.objects.create(question=question, choice_text="Not much", votes=0)
    Choice.objects.create(question=question, choice_text="The sky", votes=2)
    return question


@pytest.mark.django_db
def test_list_questions(client, question):
    response = client.get("/api/questions/")
    assert response.status_code == 200
    assert response.data["count"] == 1
    data = response.data["results"][0]
    assert data["question_text"] == "What's up?"
    assert data["total_votes"] == 2
    assert len(data["choices"]) == 2


@pytest.mark.django_db
def test_create_question_requires_login(client):
    payload = {"question_text": "New?", "pub_date": timezone.now().isoformat()}
    assert client.post("/api/questions/", payload).status_code == 403

    client.force_authenticate(User.objects.create_user("bob", password="pw"))
    response = client.post("/api/questions/", payload)
    assert response.status_code == 201
    assert Question.objects.filter(question_text="New?").exists()


@pytest.mark.django_db
def test_vote(client, question):
    choice = question.choice_set.get(choice_text="Not much")
    response = client.post(f"/api/questions/{question.id}/vote/", {"choice": choice.id})
    assert response.status_code == 200
    assert response.data["votes"] == 1


@pytest.mark.django_db
def test_vote_with_choice_of_other_question(client, question):
    other = Question.objects.create(question_text="Other", pub_date=timezone.now())
    other_choice = Choice.objects.create(question=other, choice_text="X")
    response = client.post(f"/api/questions/{question.id}/vote/", {"choice": other_choice.id})
    assert response.status_code == 404


@pytest.mark.django_db
def test_vote_without_choice(client, question):
    response = client.post(f"/api/questions/{question.id}/vote/", {})
    assert response.status_code == 400


@pytest.mark.django_db
def test_detail_page_posts_vote_to_api(question):
    response = Client().get(f"/polls/{question.id}/")
    assert response.status_code == 200
    assert f"/api/questions/{question.id}/vote/" in response.content.decode()


@pytest.mark.django_db
def test_logged_in_vote_needs_csrf_token(question):
    # même chemin que le JavaScript de detail.html pour un utilisateur connecté
    browser = Client(enforce_csrf_checks=True)
    browser.force_login(User.objects.create_user("alice", password="pw"))
    choice = question.choice_set.first()
    url = f"/api/questions/{question.id}/vote/"

    assert browser.post(url, {"choice": choice.id}, content_type="application/json").status_code == 403

    browser.get(f"/polls/{question.id}/")  # la page dépose le cookie CSRF
    token = browser.cookies["csrftoken"].value
    response = browser.post(
        url, {"choice": choice.id}, content_type="application/json", HTTP_X_CSRFTOKEN=token
    )
    assert response.status_code == 200
    assert response.data["votes"] == 1
