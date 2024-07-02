from rest_framework import serializers
from .models import Categories
from .models import EtatProduit
from .models import Produits
from .models import Enseigne, PrixProduitMagasin
from .models import PrixProduitMagasin
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id_categorie', 'nom_categorie']

        extra_kwargs = {
            'nom_categorie': {'required': True},
        }

class EtatProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatProduit
        fields = ['id_etat', 'libelle_etat']

class ProduitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produits
        fields = ['id_produit','libelle','libelle_ticket','prixttc','code_barre','id_categorie','tva','image','id_etat','date_creation_produit','date_modif_produit']

        extra_kwargs = {
            'libelle': {'required': True},
            'id_categorie': {'required': True},
            'id_etat': {'required': True},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login','password']
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['last_name'] = user.last_name
        token['first_name'] = user.first_name
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

