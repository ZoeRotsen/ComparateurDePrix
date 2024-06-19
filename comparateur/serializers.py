from rest_framework import serializers
from .models import Categories
from .models import EtatProduit

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id_categorie', 'nom_categorie']

class EtatProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatProduit
        fields = ['id_etat', 'libelle_etat']

        

    

