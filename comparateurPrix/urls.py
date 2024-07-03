"""
URL configuration for comparateurPrix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls


from comparateur import views

#Gestion de la documentation de l'api
schema_view = get_schema_view(
    openapi.Info(
        title="Documentation d'API",
        default_version='v1',
        description="Documentation de l'API du comparateur de prix de Guadeloupe",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/get/', views.CategoriesListAPIView.as_view(), name='categories-list'),
    path('categories/get/<int:id_categorie>/', views.CategoriesByIdListAPIView.as_view(), name='categories-list'),
    path('categories/create/', views.CreateCategoriesListAPIView.as_view(), name='categories-create'),
    path('categories/update/<int:id_categorie>/', views.UpdateCategoriesDetailAPIView.as_view(), name='categories-detail'),
    path('categories/delete/<int:id_categorie>/', views.DeleteCategoriesDetailAPIView.as_view(), name='categories-detail'),
    path('enseignes/get/', views.EnseigneListAPIView.as_view(), name='enseignes-list'),
    path('enseignes/get/<int:id_enseigne>/', views.EnseigneByIdListAPIView.as_view(), name='enseignes-list'),
    path('enseignes/create/', views.CreateEnseigneAPIView.as_view(), name='enseignes-list'),
    path('enseignes/update/<int:id_enseigne>/', views.UpdateEnseigneDetailAPIView.as_view(), name='enseignes-detail'),
    path('enseignes/delete/<int:id_enseigne>/', views.DeleteEnseigneDetailAPIView.as_view(), name='enseignes-detail'),
    path('prixProduitMagasin/get/', views.PrixMagasinProduitListAPIView.as_view(), name='prix_produit_magasin_list'),
    path('prixProduitMagasin/get/<int:idP>/<int:idM>/', views.PrixProduitMagasinByIdsListAPIView.as_view(), name='prix_produit_magasin_list'),
    path('prixProduitMagasin/delete/<int:idP>/<int:idM>/', views.DeletePrixProduitMagasinByIdAPIView.as_view(), name='delete_prix_produit_magasin'),
    path('prixProduitMagasin/create/', views.CreatePrixProduitMagasinAPIView.as_view(), name='create_prix_produit_magasin'),
    path('prixProduitMagasin/update/<int:idP>/<int:idM>/', views.UpdatePrixProduitMagasinAPIView.as_view(), name='update_prix_produit_magasin'),
    path('etatProduit/get/', views.EtatProduitListAPIView.as_view(), name='etatProduit-list'),
    path('etatProduit/get/<int:id_etat>/', views.EtatProduitByIdListAPIView.as_view(), name='etatProduit-list'),
    path('etatProduit/delete/<int:id_etat>/', views.DeleteEtatProduitByIdListAPIView.as_view(), name='etatProduit-delete'),
    path('etatProduit/create/', views.CreateEtatProduitAPIView.as_view(), name='etatProduit-create'),
    path('etatProduit/update/<int:id_etat>/', views.UpdateEtatProduitAPIView.as_view(), name='etatProduit-update'),
    path('produits/get/', views.ProduitsListAPIView.as_view(), name='produits-list'),
    path('produits/get/<int:id_produit>/', views.ProduitsByIdListAPIView.as_view(), name='produit-list'),
    path('produits/get/nom/<str:libelle>/', views.ProduitsByNameListAPIView.as_view(), name='produit-list'),
    path('produits/get/categorie/<int:id_categorie>/', views.ProduitsByIdCategorieListAPIView.as_view(), name='produits-list'),
    path('produits/delete/<int:id_produit>/', views.DeleteProduitsByIdListAPIView.as_view(), name='produits-delete'),
    path('produits/create/', views.CreateProduitsAPIView.as_view(), name='produits-create'),
    path('produits/update/<int:id_produit>/', views.UpdateProduitsAPIView.as_view(), name='produits-update'),
    path('utilisateurs/create/', views.CreateUtilisateursAPIView.as_view(), name='utilisateurs-create'),
    path('utilisateurs/create/lambda_connecte/', views.CreateLambdaConnecteAPIView.as_view(), name='utilisateurs-create'),
    path('utilisateurs/create/certifie/', views.CreateCertifieAPIView.as_view(), name='utilisateurs-create'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
