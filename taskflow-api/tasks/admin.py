from django.contrib import admin
from .models import Task
from django.contrib import admin

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_at')
    search_fields = ('title', 'status')

# Personnalisation de l’en-tête et des titres du site d'administration
admin.site.site_header = "TaskFlow – Administration"
admin.site.site_title = "TaskFlow Admin"
admin.site.index_title = "Tableau de bord – Gestion des tâches"