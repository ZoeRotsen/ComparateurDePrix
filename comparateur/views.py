# myapp/views.py
from rest_framework import generics
from .models import Categories
from .models import EtatProduit
from .serializers import CategoriesSerializer
from .serializers import EtatProduitSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class CategoriesListAPIView(generics.ListAPIView):
    queryset = Categories.getCategories()  # Récupère toutes les catégories depuis la base de données
    serializer_class = CategoriesSerializer

class EtatProduitListAPIView(generics.ListAPIView):
    queryset = EtatProduit.getEtatProduit()
    serializer_class = EtatProduitSerializer

class EtatProduitByIdListAPIView(generics.ListAPIView):
    serializer_class = EtatProduitSerializer
    
    def get_queryset(self):
        etat_id = self.kwargs['id']
        return EtatProduit.getEtatProduitById(etat_id)

class DeleteEtatProduitByIdListAPIView(APIView):
     def delete(self, request, id):
        try:
            etat_produit = EtatProduit.objects.get(id_etat=id)
        except EtatProduit.DoesNotExist:
            return Response({"error": "Cet état de produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        etat_produit.delete()
        return Response({"message": "EtatProduit supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
    
        
