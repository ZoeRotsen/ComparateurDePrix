from rest_framework import serializers
from .models import Categories
from .models import EtatProduit
from .models import Produits

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id_categorie', 'nom_categorie']

class EtatProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatProduit
        fields = ['id_etat', 'libelle_etat']

class ProduitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produits
        fields = ['id_produit','libelle','libelle_ticket','prixttc','code_barre','id_categorie','tva','image','id_etat','date_creation_produit','date_modif_produit']

        

    

