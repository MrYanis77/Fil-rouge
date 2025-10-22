from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_status(value):
    if value not in ["À faire", "En cours", "Fait"]:
        raise ValidationError("Statut invalide : choisir 'À faire', 'En cours' ou 'Fait'.")

class Task(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="À faire", validators=[validate_status])
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return f"{self.title} - {self.owner.username if self.owner else 'sans propriétaire'}"