from .models import Categories, Enseigne, PrixProduitMagasin
from rest_framework import serializers

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id_categorie', 'nom_categorie']


class EnseigneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseigne
        fields = [
            'id_enseigne', 'libelle', 'adresse', 'code_postal', 'ville', 
            'longitude', 'latitude', 'date_creation_enseigne', 'date_modif_enseigne'
        ]

class PrixProduitMagasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrixProduitMagasin
        fields = [
            'id_prix_produit_magasin',
            'id_produit',
            'id_magasin',
            'prix',
            'date_creation_prix_produit_magasin',
            'date_modif_prix_produit_magasin'
        ]