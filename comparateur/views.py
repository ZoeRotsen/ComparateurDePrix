# myapp/views.py
from rest_framework import generics
from .models import Categories
from .models import EtatProduit
from .models import Produits
from .serializers import CategoriesSerializer
from .serializers import EtatProduitSerializer
from .serializers import ProduitsSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

#Table Categorie
#Récupération de toutes les catégories
class CategoriesListAPIView(generics.ListAPIView):
    queryset = Categories.getCategories()  # Récupère toutes les catégories depuis la base de données
    serializer_class = CategoriesSerializer

#Table EtatProduit
#Récupération de tous les états produits
class EtatProduitListAPIView(generics.ListAPIView):
    queryset = EtatProduit.getEtatProduit()
    serializer_class = EtatProduitSerializer

#Récupération de l'état produit par l'id
class EtatProduitByIdListAPIView(generics.ListAPIView):
    serializer_class = EtatProduitSerializer
    
    def get_queryset(self):
        etat_id = self.kwargs['id']
        return EtatProduit.getEtatProduitById(etat_id)

#Suppression de l'état produit par l'id
class DeleteEtatProduitByIdListAPIView(APIView):
     def delete(self, request, id):
        try:
            etat_produit = EtatProduit.objects.get(id_etat=id)
        except EtatProduit.DoesNotExist:
            return Response({"error": "Cet état de produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        etat_produit.delete()
        return Response({"message": "EtatProduit supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)

#Création d'un état produit
class CreateEtatProduitAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EtatProduitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

#Mise à jour de l'état produit par l'id
class UpdateEtatProduitAPIView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
             etat_produit = get_object_or_404(EtatProduit, id_etat=id)
        except EtatProduit.DoesNotExist:
            return Response({"error": "Cet état de produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EtatProduitSerializer(etat_produit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Table Produit
#Récupération de tous les produits
class ProduitsListAPIView(generics.ListAPIView):
    queryset = Produits.getProduits()
    serializer_class = ProduitsSerializer

#Récupération d'un produit par l'id
class ProduitsByIdListAPIView(generics.ListAPIView):
    serializer_class = ProduitsSerializer
    
    def get_queryset(self):
        id_produit = self.kwargs['id']
        return Produits.getProduitById(id_produit)
    
#Récupération d'un produit par l'id de la catégorie
class ProduitsByIdCategorieListAPIView(generics.ListAPIView):
    serializer_class = ProduitsSerializer
    
    def get_queryset(self):
        id_categorie = self.kwargs['id']
        return Produits.getProduitByIdCategorie(id_categorie)
    
#Suppression d'un produit par l'id
class DeleteProduitsByIdListAPIView(APIView):
     def delete(self, request, id):
        try:
            produit = Produits.objects.get(id_produit=id)
        except Produits.DoesNotExist:
            return Response({"error": "Ce produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        produit.delete()
        return Response({"message": "Produit supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)

#Création d'un produit
class CreateProduitsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProduitsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

#Mise à jour d'un produit par l'id
class UpdateProduitsAPIView(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
             produit = get_object_or_404(Produits, id_produit=id)
        except Produits.DoesNotExist:
            return Response({"error": "Ce produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProduitsSerializer(produit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
