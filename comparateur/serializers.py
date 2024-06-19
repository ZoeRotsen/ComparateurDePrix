from rest_framework import serializers
from .models import Categories, Enseigne

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id_categorie', 'nom_categorie']

class EnseigneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseigne
        fields = ['id_enseigne', 'libelle', 'adresse', 'code_postal', 'ville', 'longitude', 'latitude', 'date_creation_enseigne', 'date_modif_enseigne']
