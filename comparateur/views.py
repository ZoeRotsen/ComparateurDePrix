from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Categories, Enseigne, PrixProduitMagasin
from .serializers import CategoriesSerializer, EnseigneSerializer, PrixProduitMagasinSerializer
from datetime import datetime

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
    
class PrixMagasinProduitListAPIView(generics.ListAPIView):
    queryset = PrixProduitMagasin.objects.all()  # Récupère tous les prix de produits en magasin depuis la base de données
    serializer_class = PrixProduitMagasinSerializer

# Suppression d'un produit par l'id
class DeletePrixProduitMagasinByIdAPIView(APIView):
    def delete(self, request, idP, idM, *args, **kwargs):
        try:
            prix_produit_magasin = PrixProduitMagasin.objects.get(id_produit=idP, id_magasin=idM)
        except PrixProduitMagasin.DoesNotExist:
            return Response({"error": "Ce produit dans ce magasin n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        prix_produit_magasin.delete()
        return Response({"message": "Produit supprimé avec succès du magasin"}, status=status.HTTP_204_NO_CONTENT)
    
    
# Création d'un produit
class CreatePrixProduitMagasinAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PrixProduitMagasinSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Vérifiez si l'entrée existe déjà pour éviter les doublons
                prix_produit_magasin = PrixProduitMagasin.objects.get(
                    id_produit=serializer.validated_data['id_produit'],
                    id_magasin=serializer.validated_data['id_magasin']
                )
                return Response({"error": "Cette combinaison de produit et de magasin existe déjà."}, status=status.HTTP_400_BAD_REQUEST)
            except PrixProduitMagasin.DoesNotExist:
                # Si elle n'existe pas, enregistrez la nouvelle entrée
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mise à jour d'un produit par l'id


class UpdatePrixProduitMagasinAPIView(APIView):
    def put(self, request, idP, idM, *args, **kwargs):
        try:
            prix_produit_magasin = get_object_or_404(PrixProduitMagasin, id_produit=idP, id_magasin=idM)
        except PrixProduitMagasin.DoesNotExist:
            return Response({"error": "Ce produit dans ce magasin n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        # Ajouter la date de modification actuelle
        request.data['date_modif_prix_produit_magasin'] = datetime.now().date()

        serializer = PrixProduitMagasinSerializer(prix_produit_magasin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
