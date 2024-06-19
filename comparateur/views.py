# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Categories, Enseigne
from .serializers import CategoriesSerializer, EnseigneSerializer

class CategoriesListAPIView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return Categories.get_categories()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnseigneListAPIView(generics.ListCreateAPIView):  # Utilisation de ListCreateAPIView pour autoriser POST
    queryset = Enseigne.objects.all()
    serializer_class = EnseigneSerializer

    def get_queryset(self):
        return Enseigne.get_enseignes()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
