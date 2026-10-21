from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class IndexView(View):

    def get(self, request):
        return render(request, 'accueil.html')
    
class ContactView(View):

    def get(self, request):
        return render(request, 'contact.html')
    
class AddView(View):

    def get(self, request):
        return render(request, 'add.html')
    
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    
class AddQuestionView(LoginRequiredMixin, View):
    login_url = reverse_lazy('polls:index')
    ...