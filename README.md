# TUTO DJANGO AUGMENTE

## 2.2.1

### 1 et 2
J'ai utilisé la commande `q = Question(attribut1, atttribut2)` puis `q.save()` pour sauvegarder une nouvelle question dans la base de donnée.
Enfin pour ajouter des choix aux questions j'ai fait `q.choice_set.create(attribut)`. 

### 3
Je peux filtrer et voir les attributs de mes classes Question et Choice.

### 4
J'ai bien ajouté les classes QuestionAdmin et ChoiceAdmin avec les attributs + updaté le fichier admin.py:

`class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    ordering = ["pub_date"]
    search_fields = ["question_text"]
    `

