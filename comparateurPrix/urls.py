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
from comparateur import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('categories/', views.CategoriesListCreateAPIView.as_view(), name='categories-list'),
    path('categories/<int:id_categorie>/', views.CategoriesDetailAPIView.as_view(), name='categories-detail'),
    path('enseignes/', views.EnseigneListCreateAPIView.as_view(), name='enseignes-list'),
    path('enseignes/<int:id_enseigne>/', views.EnseigneDetailAPIView.as_view(), name='enseignes-detail'),
    path('prix-produit-magasin/', views.PrixMagasinProduitListAPIView.as_view(), name='prix_produit_magasin_list'),
    path('prix-produit-magasin/<int:idP>/<int:idM>/', views.DeletePrixProduitMagasinByIdAPIView.as_view(), name='delete_prix_produit_magasin'),
    path('create-prix-produit-magasin/', views.CreatePrixProduitMagasinAPIView.as_view(), name='create_prix_produit_magasin'),
    path('update-prix-produit-magasin/<int:idP>/<int:idM>/', views.UpdatePrixProduitMagasinAPIView.as_view(), name='update_prix_produit_magasin'),
]
