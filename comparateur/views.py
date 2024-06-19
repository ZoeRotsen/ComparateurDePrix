# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Categories, Enseigne
from .serializers import CategoriesSerializer, EnseigneSerializer

