from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "home"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("add/", views.AddView.as_view(), name="add"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]