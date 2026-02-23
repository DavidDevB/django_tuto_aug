from django.contrib import admin
from .models import Question, Choice, QuestionAdmin, ChoiceAdmin

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
