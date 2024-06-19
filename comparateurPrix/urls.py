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
    path('categories/', views.CategoriesListAPIView.as_view(), name='categories-list'),
    path('etatProduit/get/', views.EtatProduitListAPIView.as_view(), name='etatProduit-list'),
    path('etatProduit/get/<int:id>/', views.EtatProduitByIdListAPIView.as_view(), name='etatProduit-list'),
    path('etatProduit/delete/<int:id>/', views.DeleteEtatProduitByIdListAPIView.as_view(), name='etatProduit-delete'),
]
