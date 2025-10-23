from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer

class BusinessRuleException(APIException):
    status_code = 400
    default_detail = "Règle métier non respectée."

class TaskViewSet(ModelViewSet):

    # ... queryset, serializer_class, filters, etc.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "En cours":
            raise BusinessRuleException("Impossible de supprimer une tâche 'En cours'.")
        return super().destroy(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "Tâche créée", "data":serializer.data}, status=status.HTTP_201_CREATED)

    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer

    # Filtres / recherche / tri
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'status']
    ordering_fields = ['created_at', 'title']
    filterset_fields = ['status']

    # AJOUT ICI : méthode d’instance dans la classe
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(owner=user)