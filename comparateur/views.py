# myapp/views.py
from rest_framework import generics
from .models import Categories
from .models import EtatProduit
from .models import Produits
from .models import Enseigne
from .models import PrixProduitMagasin
from django.contrib.auth.models import User
from .serializers import CategoriesSerializer
from .serializers import EtatProduitSerializer
from .serializers import ProduitPrixCategorieSerializer
from .serializers import ProduitPrixSerializer
from .serializers import ProduitsSerializer
from .serializers import PrixProduitMagasinSerializer
from .serializers import EnseigneSerializer
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from datetime import datetime

#Gestion des permissions
class EstLambdaConnecte(BasePermission):
    #Permission personnalisée pour vérifier si l'utilisateur appartient au groupe lambda connecté
    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est connecté
        if not request.user.is_authenticated:
            return False

        # Vérifier si l'utilisateur appartient au groupe spécifique
        group_name = 'lambda_connecté' 
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return False

        return request.user.groups.filter(name=group_name).exists()
    
class EstCertifie(BasePermission):
    #Permission personnalisée pour vérifier si l'utilisateur appartient au groupe lambda connecté
    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est connecté
        if not request.user.is_authenticated:
            return False

        # Vérifier si l'utilisateur appartient au groupe spécifique
        group_name = 'certifié' 
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return False

        return request.user.groups.filter(name=group_name).exists()
    
class EstAdministrateur(BasePermission):
   #Permission personnalisée pour vérifier si l'utilisateur appartient au groupe administrateur
    def has_permission(self, request, view):
        # Vérifier si l'utilisateur est connecté
        if not request.user.is_authenticated:
            return False

        # Vérifier si l'utilisateur appartient au groupe spécifique
        group_name = 'administrateur'  # Remplacez par le nom de votre groupe
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            return False

        return request.user.groups.filter(name=group_name).exists()
    
class EstAdministrateurOuCertifie(BasePermission):
#Permission personnalisée pour vérifier si l'utilisateur appartient au groupe administrateur ou au groupe certifié
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        allowed_groups = ['administrateur', 'certifié']
        return any(request.user.groups.filter(name=group_name).exists() for group_name in allowed_groups)
    
#Table Catégories
class CategoriesListAPIView(generics.ListAPIView):
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer

#Récupération d'une catégorie par l'id
class CategoriesByIdListAPIView(generics.ListAPIView):
    serializer_class = CategoriesSerializer
    
    def get_queryset(self):
        id_categorie = self.kwargs['id_categorie']
        return Categories.get_categorie_by_id(id_categorie)

class CreateCategoriesListAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateur]
    @swagger_auto_schema(request_body=CategoriesSerializer)
    def post(self, request, *args, **kwargs):
        nom_categorie = request.data.get('nom_categorie')
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            if nom_categorie:
                categorie = Categories.add_categorie(nom_categorie)
                categorie_serializer = CategoriesSerializer(categorie)
                return Response(categorie_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class UpdateCategoriesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateur]
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer
    lookup_field = 'id_categorie'

    @swagger_auto_schema(request_body=CategoriesSerializer)
    def put(self, request, *args, **kwargs):
        id_categorie = kwargs.get('id_categorie')
        nom_categorie = request.data.get('nom_categorie')
        try:
            categorie_instance = Categories.objects.get(id_categorie=id_categorie)
        except Categories.DoesNotExist:
            return Response({"error": "Cette catégories de produits n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategoriesSerializer(categorie_instance, data=request.data, partial=True)
        if serializer.is_valid():
            if nom_categorie:
                Categories.update_categorie(id_categorie, nom_categorie)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteCategoriesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateur]
    queryset = Categories.get_categories()
    serializer_class = CategoriesSerializer
    lookup_field = 'id_categorie'
    
    @swagger_auto_schema(request_body=CategoriesSerializer)
    def delete(self, request, *args, **kwargs):
        id_categorie = kwargs.get('id_categorie')
        Categories.delete_categorie(id_categorie)
        return Response({"message": "Catégorie supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
    
#Table Enseigne
class EnseigneListAPIView(generics.ListAPIView):
    queryset = Enseigne.get_enseignes()
    serializer_class = EnseigneSerializer

#Récupération d'une enseigne par l'id
class EnseigneByIdListAPIView(generics.ListAPIView):
    serializer_class = EnseigneSerializer
    
    def get_queryset(self):
        id_enseigne = self.kwargs['id_enseigne']
        return Enseigne.get_enseignes_by_id(id_enseigne)
    
class CreateEnseigneAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateurOuCertifie]
    @swagger_auto_schema(request_body=EnseigneSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # On récupère une copie des données
        data['date_creation_enseigne'] = timezone.now().date()  # On met à jour avec la date actuelle
        data['date_modif_enseigne'] = timezone.now().date()  # On met à jour avec la date actuelle

        serializer = EnseigneSerializer(data=data)
        if serializer.is_valid():
            enseigne = Enseigne.add_enseigne(
                data.get('libelle'),
                data.get('adresse'),
                data.get('code_postal'),
                data.get('ville'),
                data.get('longitude'),
                data.get('latitude'),
                data.get('date_creation_enseigne'),
                data.get('date_modif_enseigne')
            )
            if enseigne:
                enseigne_serializer = EnseigneSerializer(enseigne)
                return Response(enseigne_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEnseigneDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateurOuCertifie]
    queryset = Enseigne.get_enseignes()
    lookup_field = 'id_enseigne'

    @swagger_auto_schema(request_body=EnseigneSerializer)
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id_enseigne')
        try:
            enseigne_instance = Enseigne.objects.get(id_enseigne=id)
        except Enseigne.DoesNotExist:
            return Response({"error": "Cette enseigne n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()  # On récupère une copie des données
        data['date_modif_enseigne'] = timezone.now().date() #On met à jour avec la date actuelle
        serializer = EnseigneSerializer(enseigne_instance, data=data, partial=True)

        if serializer.is_valid():
            enseigne = Enseigne.update_enseigne(
                id,
                data.get('libelle'),
                data.get('adresse'),
                data.get('code_postal'),
                data.get('ville'),
                data.get('longitude'),
                data.get('latitude'),
                data.get('date_modif_enseigne')
            )
            if enseigne:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteEnseigneDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateur]
    queryset = Enseigne.get_enseignes()
    serializer_class = EnseigneSerializer
    lookup_field = 'id_enseigne'

    @swagger_auto_schema(request_body=EnseigneSerializer)
    def delete(self, request, *args, **kwargs):
        id_enseigne = kwargs.get('id_enseigne')
        Enseigne.delete_enseigne(id_enseigne)
        return Response({"message": "Enseigne supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)

#Table Prix_Produit_Magasin
class PrixMagasinProduitListAPIView(generics.ListAPIView):
    queryset = PrixProduitMagasin.objects.all()  # Récupère tous les prix de produits en magasin depuis la base de données
    serializer_class = PrixProduitMagasinSerializer

#Récupération d'un prix de produit par les id
class PrixProduitMagasinByIdsListAPIView(generics.ListAPIView):
    serializer_class = PrixProduitMagasinSerializer
    
    def get_queryset(self):
        id_produit = self.kwargs['idP']
        id_magasin = self.kwargs['idM']
        return PrixProduitMagasin.getPrixProduitMagasinByIds(id_produit,id_magasin)
    
# Suppression d'un prix de produit par l'id
class DeletePrixProduitMagasinByIdAPIView(APIView):
    permission_classes = [IsAuthenticated,EstCertifie]
    @swagger_auto_schema(request_body=PrixProduitMagasinSerializer)
    def delete(self, request, idP, idM, *args, **kwargs):
        try:
            prix_produit_magasin = PrixProduitMagasin.objects.get(id_produit=idP, id_magasin=idM)
        except PrixProduitMagasin.DoesNotExist:
            return Response({"error": "Ce produit dans ce magasin n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        prix_produit_magasin.delete()
        return Response({"message": "Produit supprimé avec succès du magasin"}, status=status.HTTP_204_NO_CONTENT)
    
    
# Création d'un prix de produit
class CreatePrixProduitMagasinAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateurOuCertifie]
    @swagger_auto_schema(request_body=PrixProduitMagasinSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # On récupère une copie des données
        data['date_creation_prix_produit_magasin'] = timezone.now().date() #On met à jour avec la date actuelle
        data['date_modif_prix_produit_magasin'] = timezone.now().date() #On met à jour avec la date actuelle
        serializer = PrixProduitMagasinSerializer(data=data)
        if serializer.is_valid():
            #try:
                # Vérifiez si l'entrée existe déjà pour éviter les doublons
                #prix_produit_magasin = PrixProduitMagasin.objects.get(
            id_produit=serializer.validated_data['id_produit'],
            id_magasin=serializer.validated_data['id_magasin']
                #)
                #return Response({"error": "Cette combinaison de produit et de magasin existe déjà."}, status=status.HTTP_400_BAD_REQUEST)
            #except PrixProduitMagasin.DoesNotExist:
                # Si elle n'existe pas, enregistrez la nouvelle entrée
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mise à jour d'un prix de produit par l'id
class UpdatePrixProduitMagasinAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateurOuCertifie]
    @swagger_auto_schema(request_body=PrixProduitMagasinSerializer)
    def put(self, request, idP, idM, *args, **kwargs):
        try:
            prix_produit_magasin = get_object_or_404(PrixProduitMagasin, id_produit=idP, id_magasin=idM)
        except PrixProduitMagasin.DoesNotExist:
            return Response({"error": "Ce produit n'existe pas dans ce magasin"}, status=status.HTTP_404_NOT_FOUND)

        # Ajouter la date de modification actuelle
        request.data['date_modif_prix_produit_magasin'] = datetime.now().date()

        serializer = PrixProduitMagasinSerializer(prix_produit_magasin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Table EtatProduit
#Récupération de tous les états produits
class EtatProduitListAPIView(generics.ListAPIView):
    queryset = EtatProduit.getEtatProduit()
    serializer_class = EtatProduitSerializer

#Récupération de l'état produit par l'id
class EtatProduitByIdListAPIView(generics.ListAPIView):
    serializer_class = EtatProduitSerializer
    
    def get_queryset(self):
        etat_id = self.kwargs['id_etat']
        return EtatProduit.getEtatProduitById(etat_id)

#Suppression de l'état produit par l'id
class DeleteEtatProduitByIdListAPIView(APIView):
    permission_classes = [IsAuthenticated,EstCertifie]
    def delete(self, request, id_etat):
        try:
            etat_produit = EtatProduit.objects.get(id_etat=id_etat)
        except EtatProduit.DoesNotExist:
            return Response({"error": "Cet état de produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        etat_produit.delete()
        return Response({"message": "Etat du produit supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)

#Création d'un état produit
class CreateEtatProduitAPIView(APIView):
    permission_classes = [IsAuthenticated,EstCertifie]
    @swagger_auto_schema(request_body=EtatProduitSerializer)
    def post(self, request, *args, **kwargs):
        serializer = EtatProduitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

#Mise à jour de l'état produit par l'id
class UpdateEtatProduitAPIView(APIView):
    permission_classes = [IsAuthenticated,EstLambdaConnecte]
    @swagger_auto_schema(request_body=EtatProduitSerializer)
    def put(self, request, id_etat, *args, **kwargs):
        try:
             etat_produit = get_object_or_404(EtatProduit, id_etat=id_etat)
        except EtatProduit.DoesNotExist:
            return Response({"error": "Cet état de produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EtatProduitSerializer(etat_produit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Table Produit
#Récupération de tous les produits
class ProduitsListAPIView(generics.ListAPIView):
    serializer_class = ProduitPrixCategorieSerializer

    @swagger_auto_schema(request_body=ProduitPrixCategorieSerializer)
    def list(self, request, *args, **kwargs):
        produits= Produits.getProduits()
        response_data = []

        for produit in produits:
            produit_data = ProduitsSerializer(produit).data

            # Récupérer le prix le plus récent
            prix = PrixProduitMagasin.objects.filter(id_produit=produit.id_produit).order_by('-date_creation_prix_produit_magasin').first()
            if prix:
                prix_data = PrixProduitMagasinSerializer(prix).data
                produit_data['prix'] = prix_data
            else:
                produit_data['prix'] = None

            # Récupérer la catégorie
            if produit.id_categorie:
                categorie = Categories.objects.get(pk=produit.id_categorie.pk)
                if categorie:
                    categorie_data = CategoriesSerializer(categorie).data
                    produit_data['categorie'] = categorie_data
                else:
                    produit_data['categorie'] = None
            else:
                produit_data['categorie'] = None
                
            response_data.append(produit_data)

        return Response(response_data, status=status.HTTP_200_OK)

#Récupération d'un produit par l'id
class ProduitsByIdListAPIView(generics.ListAPIView):
    serializer_class = ProduitPrixCategorieSerializer

    @swagger_auto_schema(responses={200: ProduitPrixCategorieSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        id_produit = self.kwargs['id_produit']
        produit= Produits.getProduitById(id_produit)
        response_data = []

        produit_data = ProduitsSerializer(produit).data
        # Récupérer le prix le plus récent
        prix = PrixProduitMagasin.objects.filter(id_produit=produit.id_produit).order_by('-date_creation_prix_produit_magasin').first()
        if prix:
            prix_data = PrixProduitMagasinSerializer(prix).data
            produit_data['prix'] = prix_data
        else:
            produit_data['prix'] = None

        # Récupérer la catégorie
        if produit.id_categorie:
            categorie = Categories.objects.get(pk=produit.id_categorie.pk)
            if categorie:
                categorie_data = CategoriesSerializer(categorie).data
                produit_data['categorie'] = categorie_data
            else:
                produit_data['categorie'] = None
        else:
            produit_data['categorie'] = None

        response_data.append(produit_data)

        return Response(response_data, status=status.HTTP_200_OK)
    
#Récupération d'un produit par le nom
class ProduitsByNameListAPIView(generics.ListAPIView):
    serializer_class = ProduitPrixCategorieSerializer
    @swagger_auto_schema(request_body=ProduitPrixCategorieSerializer)
    def list(self, request, *args, **kwargs):
        libelle = self.kwargs['libelle']
        produits= Produits.getProduitsByName(libelle)
        response_data = []

        for produit in produits:
            produit_data = ProduitsSerializer(produit).data
            # Récupérer le prix le plus récent
            prix = PrixProduitMagasin.objects.filter(id_produit=produit.id_produit).order_by('-date_creation_prix_produit_magasin').first()
            if prix:
                prix_data = PrixProduitMagasinSerializer(prix).data
                produit_data['prix'] = prix_data
            else:
                produit_data['prix'] = None

           # Récupérer la catégorie
            if produit.id_categorie:
                categorie = Categories.objects.get(pk=produit.id_categorie.pk)
                if categorie:
                    categorie_data = CategoriesSerializer(categorie).data
                    produit_data['categorie'] = categorie_data
                else:
                    produit_data['categorie'] = None
            else:
                produit_data['categorie'] = None
            
            response_data.append(produit_data)

        return Response(response_data, status=status.HTTP_200_OK)

        
    
#Récupération d'un produit par l'id de la catégorie
class ProduitsByIdCategorieListAPIView(generics.ListAPIView):
    serializer_class = ProduitPrixCategorieSerializer
    
    def list(self, request, *args, **kwargs):
        id_categorie = self.kwargs['id_categorie']
        produits = Produits.getProduitByIdCategorie(id_categorie)
        response_data = []

        for produit in produits:
            produit_data = ProduitsSerializer(produit).data
            # Récupérer le prix le plus récent
            prix = PrixProduitMagasin.objects.filter(id_produit=produit.id_produit).order_by('-date_creation_prix_produit_magasin').first()
            if prix:
                prix_data = PrixProduitMagasinSerializer(prix).data
                produit_data['prix'] = prix_data
            else:
                produit_data['prix'] = None

           # Récupérer la catégorie
            if produit.id_categorie:
                categorie = Categories.objects.get(pk=produit.id_categorie.pk)
                if categorie:
                    categorie_data = CategoriesSerializer(categorie).data
                    produit_data['categorie'] = categorie_data
                else:
                    produit_data['categorie'] = None
            else:
                produit_data['categorie'] = None
            
            response_data.append(produit_data)

        return Response(response_data, status=status.HTTP_200_OK)

#Création du produit avec son prix
class CreateProduitEtPrixAPIView(APIView):
    permission_classes = [IsAuthenticated, EstAdministrateurOuCertifie]

    @swagger_auto_schema(request_body=ProduitPrixSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        # Ajouter la date de création/modification pour le produit et le prix
        data['date_creation_produit'] = timezone.now().date()
        data['date_modif_produit'] = timezone.now().date()
        data['date_creation_prix_produit_magasin'] = timezone.now().date()
        data['date_modif_prix_produit_magasin'] = timezone.now().date()

        # Serializer pour le produit
        produit_serializer = ProduitsSerializer(data=data)

        # Serializer pour le prix de produit magasin
        prix_serializer = PrixProduitMagasinSerializer(data=data)

        if produit_serializer.is_valid():
            if prix_serializer.is_valid():
                # Sauvegarde du produit
                produit = produit_serializer.save()
                data['id_produit'] = produit.id_produit
                # Serializer pour le prix de produit magasin avec le nouvel ID de produit
                #try:
                    # Vérifier si une entrée existe déjà pour éviter les doublons
                    #PrixProduitMagasin.objects.get(
                        #id_produit=data['id_produit'],
                        #id_magasin=data['id_magasin']
                    #)
                    #return Response({"error": "Cette combinaison de produit et de magasin existe déjà."}, status=status.HTTP_400_BAD_REQUEST)
                #except PrixProduitMagasin.DoesNotExist:
                # Ssauvegarder le prix de produit magasin
                prix_serializer = PrixProduitMagasinSerializer(data=data)
                if prix_serializer.is_valid():
                    prix_produit_magasin = prix_serializer.save()
                    return Response({"produit": produit_serializer.data, "prix": prix_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(prix_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(produit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    
#Suppression d'un produit par l'id
class DeleteProduitsByIdListAPIView(APIView):
    permission_classes = [IsAuthenticated,EstCertifie]
    def delete(self, request, id_produit):
        try:
            produit = Produits.objects.get(id_produit=id_produit)
        except Produits.DoesNotExist:
            return Response({"error": "Ce produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

        produit.delete()
        return Response({"message": "Produit supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)

#Création d'un produit
class CreateProduitsAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateurOuCertifie]
    @swagger_auto_schema(request_body=ProduitsSerializer)
    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # On récupère une copie des données
        data['date_creation_produit'] = timezone.now().date() #On met à jour avec la date actuelle
        data['date_modif_produit'] = timezone.now().date() #On met à jour avec la date actuelle
        serializer = ProduitsSerializer(data=data)
        if serializer.is_valid():
            produit=serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

#Mise à jour d'un produit par l'id
class UpdateProduitsAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateurOuCertifie]
    @swagger_auto_schema(request_body=ProduitsSerializer)
    def put(self, request, id_produit, *args, **kwargs):
        try:
             produit = get_object_or_404(Produits, id_produit=id_produit)
        except Produits.DoesNotExist:
            return Response({"error": "Ce produit n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()  # On récupère une copie des données
        data['date_modif_produit'] = timezone.now().date() #On met à jour avec la date actuelle
        serializer = ProduitsSerializer(produit, data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Table Utilisateurs
class CreateUtilisateursAPIView(APIView):
     @swagger_auto_schema(request_body=UserSerializer)
     def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve validated data from serializer
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']
            nom = serializer.validated_data.get('last_name', '')  # Optional fields
            prenom = serializer.validated_data.get('first_name', '')  # Optional fields

            # Create user using Django's create_user method
            user = User.objects.create_user(email=email, password=password, username=username)  # Using email as username

            # Set optional fields if available
            user.first_name = prenom
            user.last_name = nom

            # Save user object
            user.save()

            # Return successful response with user details
            return Response({'message': 'Utilisateur créé avec succès', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
            # Return errors if data is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

#Création d'un utilisateur qui est directement ajouté au groupe lamda_connecté
class CreateLambdaConnecteAPIView(APIView):
    
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérer les données validées
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']
            nom = serializer.validated_data.get('last_name', '')  # Optional fields
            prenom = serializer.validated_data.get('first_name', '')  # Optional fields

            # Créer l'utilisateur en utilisant CustomUserManager
            user = User.objects.create_user(email=email, password=password, username=username)

            # Set optional fields if available
            user.first_name = prenom
            user.last_name = nom

            # Save user object
            user.save()

            # Ajouter l'utilisateur au groupe spécifique
            group_name = 'lambda_connecté' 
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                # Gérer l'erreur si le groupe spécifié n'existe pas
                return Response({'error': f'Le groupe "{group_name}" n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)

            # Vous pouvez ajouter d'autres champs personnalisés ici

            # Renvoyer une réponse avec les détails de l'utilisateur créé
            return Response({'message': 'Utilisateur créé avec succès', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
            # Si les données ne sont pas valides, renvoyer les erreurs
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#Création d'un utilisateur qui est directement ajouté au groupe certifié
class CreateCertifieAPIView(APIView):
    permission_classes = [IsAuthenticated,EstAdministrateur]
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Récupérer les données validées
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            username = serializer.validated_data['username']
            nom = serializer.validated_data.get('last_name', '')  # Optional fields
            prenom = serializer.validated_data.get('first_name', '')  # Optional fields

            # Créer l'utilisateur en utilisant CustomUserManager
            user = User.objects.create_user(email=email, password=password, username=username)

            # Set optional fields if available
            user.first_name = prenom
            user.last_name = nom

            # Save user object
            user.save()

            # Ajouter l'utilisateur au groupe spécifique
            group_name = 'certifié' 
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                # Gérer l'erreur si le groupe spécifié n'existe pas
                return Response({'error': f'Le groupe "{group_name}" n\'existe pas.'}, status=status.HTTP_404_NOT_FOUND)

            # Vous pouvez ajouter d'autres champs personnalisés ici

            # Renvoyer une réponse avec les détails de l'utilisateur créé
            return Response({'message': 'Utilisateur créé avec succès', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
            # Si les données ne sont pas valides, renvoyer les erreurs
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
