# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.hashers import make_password



class Categories(models.Model):
    id_categorie = models.AutoField(db_column='ID_categorie', primary_key=True)  # Field name made lowercase.
    nom_categorie = models.CharField(db_column='Nom_categorie', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categories'

    @classmethod
    def get_categories(cls):
        return cls.objects.all()
    
    @classmethod
    def get_categorie_by_id(cls,id):
        try:
            return cls.objects.filter(id_categorie=id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def add_categorie(cls, nom):
        return cls.objects.create(nom_categorie=nom)

    @classmethod
    def delete_categorie(cls, id_categorie):
        return cls.objects.filter(id_categorie=id_categorie).delete()

    @classmethod
    def update_categorie(cls, id_categorie, nom):
        return cls.objects.filter(id_categorie=id_categorie).update(nom_categorie=nom)


class Enseigne(models.Model):
    id_enseigne = models.AutoField(db_column='ID_enseigne', primary_key=True)  # Field name made lowercase.
    libelle = models.CharField(db_column='Libelle', max_length=127, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=255, blank=True, null=True)  # Field name made lowercase.
    code_postal = models.IntegerField(db_column='Code_postal', blank=True, null=True)  # Field name made lowercase.
    ville = models.CharField(db_column='Ville', max_length=50, blank=True, null=True)  # Field name made lowercase.
    longitude = models.DecimalField(db_column='Longitude', max_digits=65535, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    latitude = models.DecimalField(db_column='Latitude', max_digits=65535, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    date_creation_enseigne = models.DateField(db_column='Date_creation_Enseigne', blank=True, null=True)  # Field name made lowercase.
    date_modif_enseigne = models.DateField(db_column='Date_modif_Enseigne', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Enseigne'

    @classmethod
    def get_enseignes(cls):
        return cls.objects.all()
    
    @classmethod
    def get_enseignes_by_id(cls,id):
        try:
            return cls.objects.filter(id_enseigne=id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def add_enseigne(cls, libelle, adresse, code_postal, ville, longitude, latitude, date_creation_enseigne, date_modif_enseigne):
        enseigne= cls.objects.create(
            libelle=libelle,
            adresse=adresse,
            code_postal=code_postal,
            ville=ville,
            longitude=longitude,
            latitude=latitude,
            date_creation_enseigne=date_creation_enseigne,
            date_modif_enseigne=date_modif_enseigne
        )
        return enseigne

    @classmethod
    def delete_enseigne(cls, id_enseigne):
        return cls.objects.filter(id_enseigne=id_enseigne).delete()

    @classmethod
    def update_enseigne(cls, id_enseigne, libelle, adresse, code_postal, ville, longitude, latitude,date_modif_enseigne):
        return cls.objects.filter(id_enseigne=id_enseigne).update(
            libelle=libelle,
            adresse=adresse,
            code_postal=code_postal,
            ville=ville,
            longitude=longitude,
            latitude=latitude,
            date_modif_enseigne=date_modif_enseigne
        )

    
class EtatProduit(models.Model):
    id_etat = models.AutoField(db_column='ID_etat', primary_key=True)  # Field name made lowercase.
    libelle_etat = models.CharField(db_column='Libelle_etat', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Etat_Produit'
    
    @classmethod
    def getEtatProduit(cls):
        return cls.objects.all()
    
    @classmethod
    def getEtatProduitById(cls,id):
        try:
            return cls.objects.filter(id_etat=id)
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def deleteEtatProduit(cls, id):
        try:
            objetEtatProduit = cls.objects.filter(id)
            objetEtatProduit.delete()
        except cls.DoesNotExist:
            return None


class PrixProduitMagasin(models.Model):
    id_prix_produit_magasin = models.AutoField(db_column='ID_prix_Produit_Magasin', primary_key=True)  # Field name made lowercase.
    id_produit = models.ForeignKey('Produits', models.DO_NOTHING, db_column='ID_produit', blank=True, null=True)  # Field name made lowercase.
    id_magasin = models.ForeignKey(Enseigne, models.DO_NOTHING, db_column='ID_magasin', blank=True, null=True)  # Field name made lowercase.
    prix = models.DecimalField(db_column='Prix', max_digits=65535, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    date_creation_prix_produit_magasin = models.DateField(db_column='Date_creation_prix_Produit_Magasin', blank=True, null=True)  # Field name made lowercase.
    date_modif_prix_produit_magasin = models.DateField(db_column='Date_modif_prix_Produit_Magasin', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prix_Produit_Magasin'

    @classmethod
    def getPrixProduitMagasinByIds(cls,idP,idM):
        try:
            return cls.objects.filter(id_produit=idP,id_magasin=idM)
        except cls.DoesNotExist:
            return None


class Produits(models.Model):
    id_produit = models.AutoField(db_column='ID_produit', primary_key=True)  # Field name made lowercase.
    libelle = models.CharField(db_column='Libelle', max_length=255, blank=True, null=True,)  # Field name made lowercase.
    libelle_ticket = models.CharField(db_column='Libelle_Ticket', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prixttc = models.DecimalField(db_column='PrixTTC', max_digits=65535, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    code_barre = models.CharField(db_column='Code_barre', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_categorie = models.ForeignKey(Categories, models.DO_NOTHING, db_column='ID_categorie', blank=True, null=True)  # Field name made lowercase.
    tva = models.DecimalField(db_column='TVA', max_digits=65535, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_etat = models.ForeignKey(EtatProduit, models.DO_NOTHING, db_column='Id_Etat', blank=True, null=True)  # Field name made lowercase.
    date_creation_produit = models.DateField(db_column='Date_creation_Produit', blank=True, null=True)  # Field name made lowercase.
    date_modif_produit = models.DateField(db_column='Date_modif_Produit', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Produits'

    @classmethod
    def getProduits(cls):
        return cls.objects.all()
    
    @classmethod
    def getProduitById(cls,id):
        try:
            return cls.objects.filter(id_produit=id)
        except cls.DoesNotExist:
            return None

    @classmethod  
    def getProduitsByName(cls,libelle):
        try:
            return cls.objects.filter(libelle__icontains=libelle)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def getProduitByIdCategorie(cls,id):
        try:
            return cls.objects.filter(id_categorie=id)
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def deleteProduit(cls, id):
        try:
            objetProduit = cls.objects.filter(id)
            objetProduit.delete()
        except cls.DoesNotExist:
            return None


class TypeUtilisateur(models.Model):
    id_type_utilisateur = models.AutoField(db_column='ID_type_utilisateur', primary_key=True)  # Field name made lowercase.
    libelle_type = models.CharField(db_column='Libelle_type', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Type_Utilisateur'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email doit être saisi')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        # Hasher le mot de passe avant de l'enregistrer
        if password:
            user.password = make_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Utilisateurs(AbstractBaseUser):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id_type_utilisateur = models.ForeignKey(TypeUtilisateur, models.DO_NOTHING, db_column='Id_type_utilisateur', blank=True, null=True)  # Field name made lowercase.
    date_creation_utilisateurs = models.DateField(db_column='Date_creation_Utilisateurs', blank=True, null=True)  # Field name made lowercase.
    date_modif_utilisateurs = models.DateField(db_column='Date_modif_Utilisateurs', blank=True, null=True)  # Field name made lowercase.
    last_login = models.DateField(db_column='Last_login', blank=True, null=True) 
    
    is_active = models.BooleanField(default=True)
    #Avoir accès à l'interface d'administration
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        managed = False
        db_table = 'Utilisateurs'

    def __str__(self):
        return self.email

    def get_nom_complet(self):
        return f'{self.prenom} {self.nom}'

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
    
    def check_password(self, raw_password):
        #Vérifie si le mot de passe fourni correspond au mot de passe hashé dans la base de données.
        return django_check_password(raw_password, self.password)
