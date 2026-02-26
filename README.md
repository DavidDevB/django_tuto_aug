# TUTO DJANGO AUGMENTE

# 2 Tutoriel augmenté, parties 1 et 2

## Exercices sur les parties 1 et 2

### 2.2.1 Exercice d'administration

#### 2.2.1.1 et 2.2.1.2
J'ai utilisé la commande `q = Question(attribut1, atttribut2)` puis `q.save()` pour sauvegarder une nouvelle question dans la base de donnée.
Enfin pour ajouter des choix aux questions j'ai fait `q.choice_set.create(attribut)`. 

#### 2.2.1.3
Pour afficher les attributs j'ai utilisé `variable = Model.objects.first()`, puis `variable.attribut` selon l'attribut que je veux afficher.

Pour filtrer j'ai utilisé Model.objects.filter(attribut = value).

Pour trier j'ai utilisé Model.objects.order_by(attribut).

Pour trouver un contenu dans chaque champ j'ai utilsié __contains à la suite de l'attribut dans un filter().

#### 2.2.1.4
J'ai bien ajouté les classes QuestionAdmin et ChoiceAdmin avec les attributs + updaté le fichier admin.py:

```
class QuestionAdmin(admin.ModelAdmin): 
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"] 
    ordering = ["pub_date"] 
    search_fields = ["question_text"]
```

#### 2.2.1.5
J'ai réussi à créé un utilisateur avec la commande `User.objects.create_user()`. Mais je ne peux pas me connecter car je ne suis pas admin.

#### 2.2.1.6 et 2.2.1.7
J'ai bien changé le mdp de l'utilisateur dans les menus et ensuite j'ai désactivé son compte via le compte administrateur.

### 2.2.2 Exercice shell

#### 2.2.2.2.1
Ici j'ai utilisé une boucle for et un print():
```
for q in Question.objects.all():      
...     print(q.question_text, q.pub_date)
... 
What's up? 2026-02-23 12:42:28.904613+00:00
What is your favorite color? 2026-02-24 13:19:08.554262+00:00
What is your favorite dish? 2026-02-25 13:26:25.631993+00:00
In which century were you born? 2026-02-26 13:28:28.424267+00:00
What is you favorite animal? 2026-02-27 13:30:37.221658+00:00
In which country is the city of Mulhouse? 2026-02-28 13:34:46.784244+00:00
```

#### 2.2.2.2.2
J'ai utilisé la méthode .filter():

```
Question.objects.filter(pub_date__year=2026)
<QuerySet [<Question: What's up?>, <Question: What is your favorite color?>, <Question: What is your favorite dish?>, <Question: In which century were you born?>, <Question: What is you favorite animal?>, <Question: In which country is the city of Mulhouse?>]>
``` 

#### 2.2.2.2.3
```
>>> q = Question.objects.get(id=1)
>>> print(q.question_text, q.pub_date)
What's up? 2026-02-23 12:42:28.904613+00:00
>>> 
>>> for choice in q.choice_set.all():
...     print(choice.choice_text, choice.votes)
... 
Not much 0
The sky 0
```

#### 2.2.2.2.4
```
for q in Question.objects.all():
    print(q.question_text, q.pub_date)
    for choice in q.choice_set.all():
        print(choice.choice_text, choice.votes)
```

donne:
```
What's up? 2026-02-23 12:42:28.904613+00:00
Not much 0
The sky 0
What is your favorite color? 2026-02-24 13:19:08.554262+00:00
Red 0
Blue 0
Yellow 0
What is your favorite dish? 2026-02-25 13:26:25.631993+00:00
Noodles 0
Hamburger 0
Quiche 0
In which century were you born? 2026-02-26 13:28:28.424267+00:00
Twentieth 0
First 0
Twenty-first 0
What is you favorite animal? 2026-02-27 13:30:37.221658+00:00
Dolphin 0
Spider 0
Mongoose 0
In which country is the city of Mulhouse? 2026-02-28 13:34:46.784244+00:00
China 0
Groenland 0
France 0
```

#### 2.2.2.2.5
```
for q in Question.objects.all():
    q.choice_set.count()
```
donne:
```
2
3
3
3
3
3
3
3
3
```

#### 2.2.2.2.6 (optionnel)

#### 2.2.2.2.7
`Question.objects.all().order_by("-pub_date")`
donne
```
<QuerySet [<Question: In which country is the city of Mulhouse?>, <Question: What is you favorite animal?>, <Question: In which century were you born?>, <Question: What is your favorite dish?>, <Question: What is your favorite color?>, <Question: What's up?>]>
```

#### 2.2.2.2.8 (optionnel)

#### 2.2.2.2.9
```
from django.utils import timezone
>>> import datetime
>>> Question.objects.create(question_text="Combien y a-t-il de jours dans la semaine ?", pub_date=timezone.now() - datetime.timedelta(days=2))
<Question: Combien y a-t-il de jours dans la semaine ?>
```

#### 2.2.2.2.10
```
>>> q = Question.objects.get(id=7)
>>> q.choice_set.create(choice_text="7", votes=0)
<Choice: 7>
>>> q.choice_set.create(choice_text="25", votes=0)
<Choice: 25>
>>> q.choice_set.create(choice_text="1", votes=0) 
<Choice: 1>
```

#### 2.2.2.2.11
`Question.objects.all()`
donne:
```
<QuerySet [<Question: What's up?>, <Question: What is your favorite color?>, <Question: What is your favorite dish?>, <Question: In which century were you born?>, <Question: What is you favorite animal?>, <Question: In which country is the city of Mulhouse?>, <Question: Combien y a-t-il de jours dans la semaine ?>]>
```

#### 2.2.2.2.12 (optionnel)

### 2.2.3 Exercice d'écriture de méthodes du modèle (optionnel)

# 3 Tutoriel augmenté, parties 3 et 4

## 3.2 Exercices sur les parties 3 et 4

### 3.2.1
`<p>{{ question.pub_date }}</p>`

### 3.2.2
J'ai ajouté à `views.py` la vue `all`.
Ensuite j'ai ajouté l'url `all`à `urls.py`.
Enfin j'ai créé le template `all.html`.

### 3.2.3
Ajout de:
```
def get_percentage(self):
        total_votes = self.question.choice_set.aggregate(models.Sum("votes"))["votes__sum"] or 0
        if total_votes > 0:
            return (self.votes / total_votes) * 100
        else:
            return 0
```
au model Choice puis intégration dans le gabarit frequency.html: {{ choice.get_percentage }}

### 3.2.4
Ajout des méthodes dans models.py (Question):

```
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
```
Ajout de get_context_data dans views.py:
```
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_questions'] = Question.objects.count()
        context['total_votes'] = Choice.objects.aggregate(
            total=models.Sum("votes")
        )["total"] or 0
        context['total_choices'] = Choice.objects.count()
        return context
```

statistics.html:
```
<p>Total questions: {{ questions.count }}</p>
<p>Total choices: {{ total_choices }}</p>
{% for question in questions %}
    <p>{{ question.question_text }}</p>
    <p>Total votes: {{ question.total_votes }}</p>
    <p>Average votes per question: {{ question.average_votes_per_question }}</p>
    {% for choice in question.choices.all %}
        <p>{{ choice.choice_text }}: {{ choice.votes }}</p>
    {% endfor %}
{% endfor %}
```
### 3.2.5
J'ai ajouté l'ur de `form` au path et créé le fichier `form.html` avec la view en conséquence.

### 3.2.6
les méthodes get et post ont été ajoutées a views.py (QuestionFormView):
```
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
```
