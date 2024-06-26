from rest_framework import generics, status
from rest_framework.response import Response
from .models import Categories, Enseigne
from .serializers import CategoriesSerializer, EnseigneSerializer

class CategoriesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer

    def post(self, request, *args, **kwargs):
        nom_categorie = request.data.get('nom_categorie')
        if nom_categorie:
            categorie = Categories.add_categorie(nom_categorie)
            serializer = self.get_serializer(categorie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class CategoriesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer
    lookup_field = 'id_categorie'

    def delete(self, request, *args, **kwargs):
        id_categorie = kwargs.get('id_categorie')
        Categories.delete_categorie(id_categorie)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        id_categorie = kwargs.get('id_categorie')
        nom_categorie = request.data.get('nom_categorie')
        if nom_categorie:
            Categories.update_categorie(id_categorie, nom_categorie)
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class EnseigneListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enseigne.get_enseignes()
    serializer_class = EnseigneSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        enseigne = Enseigne.add_enseigne(
            data.get('libelle'),
            data.get('adresse'),
            data.get('code_postal'),
            data.get('ville'),
            data.get('longitude'),
            data.get('latitude')
        )
        if enseigne:
            serializer = self.get_serializer(enseigne)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class EnseigneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enseigne.get_enseignes()
    serializer_class = EnseigneSerializer
    lookup_field = 'id_enseigne'

    def delete(self, request, *args, **kwargs):
        id_enseigne = kwargs.get('id_enseigne')
        Enseigne.delete_enseigne(id_enseigne)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        id_enseigne = kwargs.get('id_enseigne')
        data = request.data

        enseigne = Enseigne.update_enseigne(
            id_enseigne,
            data.get('libelle'),
            data.get('adresse'),
            data.get('code_postal'),
            data.get('ville'),
            data.get('longitude'),
            data.get('latitude')
        )

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
