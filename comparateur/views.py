# myapp/views.py
from rest_framework import generics
from .models import Categories
from .serializers import CategoriesSerializer

class CategoriesListAPIView(generics.ListAPIView):
    queryset = Categories.getCategories()  # Récupère toutes les catégories depuis la base de données
    serializer_class = CategoriesSerializer
