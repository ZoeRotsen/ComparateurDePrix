# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    id_categorie = models.AutoField(db_column='ID_categorie', primary_key=True)  # Field name made lowercase.
    nom_categorie = models.CharField(db_column='Nom_categorie', max_length=127, blank=True, null=True)  # Field name made lowercase.
    date_creation_categorie = models.DateField(db_column='Date_creation_categorie', blank=True, null=True)  # Field name made lowercase.
    date_modif_categorie = models.DateField(db_column='Date_modif_categorie', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categories'

    @classmethod
    def getCategories(cls):
        return cls.objects.all()


class Enseigne(models.Model):
    id_enseigne = models.AutoField(db_column='ID_enseigne', primary_key=True)  # Field name made lowercase.
    libelle = models.CharField(db_column='Libelle', max_length=127, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adres_code_postal = models.IntegerField(db_column='Adres_code_postal', blank=True, null=True)  # Field name made lowercase.
    adres_commune = models.CharField(db_column='Adres_commune', max_length=50, blank=True, null=True)  # Field name made lowercase.
    longitude = models.DecimalField(db_column='Longitude', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    latitude = models.DecimalField(db_column='Latitude', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    date_creation_enseigne = models.DateField(db_column='Date_creation_Enseigne', blank=True, null=True)  # Field name made lowercase.
    date_modif_enseigne = models.DateField(db_column='Date_modif_Enseigne', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Enseigne'


class EtatProduit(models.Model):
    id_etat = models.AutoField(db_column='ID_etat', primary_key=True)  # Field name made lowercase.
    libelle_etat = models.CharField(db_column='Libelle_etat', max_length=127, blank=True, null=True)  # Field name made lowercase.
    date_creation_etat_produit = models.DateField(db_column='Date_creation_Etat_Produit', blank=True, null=True)  # Field name made lowercase.
    date_modif_etat_produit = models.DateField(db_column='Date_modif_Etat_Produit', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Etat_Produit'


class PrixProduitMagasin(models.Model):
    id_prix_produit_magasin = models.AutoField(db_column='ID_prix_Produit_Magasin', primary_key=True)  # Field name made lowercase.
    id_produit = models.ForeignKey('Produit', models.DO_NOTHING, db_column='ID_produit', blank=True, null=True)  # Field name made lowercase.
    id_magasin = models.ForeignKey(Enseigne, models.DO_NOTHING, db_column='ID_magasin', blank=True, null=True)  # Field name made lowercase.
    id_etat = models.ForeignKey(EtatProduit, models.DO_NOTHING, db_column='ID_etat', blank=True, null=True)  # Field name made lowercase.
    prix = models.DecimalField(db_column='Prix', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    date_creation_prix_produit_magasin = models.DateField(db_column='Date_creation_prix_Produit_Magasin', blank=True, null=True)  # Field name made lowercase.
    date_modif_prix_produit_magasin = models.DateField(db_column='Date_modif_prix_Produit_Magasin', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prix_Produit_Magasin'


class Produit(models.Model):
    id_produit = models.AutoField(db_column='ID_produit', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    code_barre = models.CharField(db_column='Code_barre', max_length=127, blank=True, null=True)  # Field name made lowercase.
    id_categorie = models.ForeignKey(Categories, models.DO_NOTHING, db_column='ID_categorie', blank=True, null=True)  # Field name made lowercase.
    tva = models.DecimalField(db_column='TVA', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=127, blank=True, null=True)  # Field name made lowercase.
    date_creation_produit = models.DateField(db_column='Date_creation_Produit', blank=True, null=True)  # Field name made lowercase.
    date_modif_produit = models.DateField(db_column='Date_modif_Produit', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Produit'


class TypeUtilisateur(models.Model):
    id_type_utilisateur = models.AutoField(db_column='ID_type_utilisateur', primary_key=True)  # Field name made lowercase.
    libelle_type = models.CharField(db_column='Libelle_type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_creation_type_utilisateur = models.DateField(db_column='Date_creation_Type_Utilisateur', blank=True, null=True)  # Field name made lowercase.
    date_modif_type_utilisateur = models.DateField(db_column='Date_modif_Type_Utilisateur', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Type_Utilisateur'


class Utilisateurs(models.Model):
    id_utilisateur = models.AutoField(db_column='ID_utilisateur', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=127, blank=True, null=True)  # Field name made lowercase.
    mot_de_passe = models.CharField(db_column='Mot_de_passe', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id_type_utilisateur = models.ForeignKey(TypeUtilisateur, models.DO_NOTHING, db_column='Id_type_utilisateur', blank=True, null=True)  # Field name made lowercase.
    date_creation_utilisateurs = models.DateField(db_column='Date_creation_Utilisateurs', blank=True, null=True)  # Field name made lowercase.
    date_modif_utilisateurs = models.DateField(db_column='Date_modif_Utilisateurs', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Utilisateurs'
