from rest_framework import generics, status
from rest_framework.response import Response
from .models import Categories, Enseigne
from .serializers import CategoriesSerializer, EnseigneSerializer

class CategoriesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer
    lookup_field = 'id_categorie'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnseigneListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enseigne.get_enseignes()
    serializer_class = EnseigneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EnseigneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enseigne.get_enseignes()
    serializer_class = EnseigneSerializer
    lookup_field = 'id_enseigne'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
