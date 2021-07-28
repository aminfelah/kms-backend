

from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
#class pour l 'information de l'utilsateur
class User(AbstractUser):
        name = models.CharField(max_length=255)
        email = models.CharField(max_length=255, unique=True)
        password = models.CharField(max_length=255)
        date_naissance = models.DateField(null=True)
        fonction = models.CharField(max_length=100)

        username = None

        objects = CustomUserManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        def __str__(self):
            return self.email

class Commande(models.Model):
    num_cmd = models.IntegerField()
    num_lots = models.IntegerField()
    dateHeure_debut = models.DateTimeField()
    dateHeure_Fin = models.DateTimeField()

class Client(models.Model):
    nomClient = models.CharField(max_length=80)
    numtel = models.IntegerField()
    email = models.EmailField()
    cmd = models.ForeignKey(Commande, on_delete=models.CASCADE)

class Tache(models.Model):
    nom_tache = models.CharField(max_length=40)
    dateHeure_debut = models.DateTimeField()
    dateHeure_Fin = models.DateTimeField()
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)

    def __str__(self):
              return self.nom_tache

class ResponsablePrincipal(models.Model):
  Nom_prenomRp = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rp')
  tacheRp = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='tacherp')

class Detecteur(models.Model):

 Nom_Det = models.ForeignKey(User, on_delete=models.CASCADE, related_name='det')
 tacheDet = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='tachedet')

class Contribuer (models.Model):
        Nom_prenomC = models.ManyToManyField(User,related_name='contribuer')
        tacheC = models.ForeignKey(Tache,on_delete=models.CASCADE,related_name='tachecon')

class Informer (models.Model):
 Nom_prenomI = models.ForeignKey(User,on_delete=models.CASCADE,related_name='informer')
 tacheI = models.ForeignKey(Tache,on_delete=models.CASCADE,related_name='tacheinfo')

class SousCause(models.Model):
     ISHIKAWA = (
         # milieu
         ('depot', 'depot'),
         ('usine', 'usine'),
         ('matiére', 'matiére'),
         ('main d oeuvre', 'main d oeuvre'),
         ('machine embalage', 'machine embalage'),
         ('batteur', 'batteur'),
         ('methode', 'methode'),

     )

     ishikawa = models.CharField(choices=ISHIKAWA, default='depot', max_length=200)
     descriptionSousCause = models.CharField(max_length=200)

     def __str__(self):
         return self.descriptionSousCause

#sous cons du catalogue
class SousConsequance(models.Model):
     descriptionSousCons = models.CharField(max_length=200)

     def __str__(self):
         return self.descriptionSousCons

class Cause(models.Model):
    ISHIKAWA = (
        # milieu
        ('depot', 'depot'),
        ('usine', 'usine'),
        ('matiére', 'matiére'),
        ('main d oeuvre', 'main d oeuvre'),
        ('machine embalage', 'machine embalage'),
        ('batteur', 'batteur'),
        ('methode', 'methode'),

    )

    ishikawa = models.CharField(choices=ISHIKAWA, default='depot',max_length=200)
    descriptionCause = models.CharField(max_length=200)
    contribuerC = models.ForeignKey(Contribuer, on_delete=models.CASCADE, null=True)
    sousCause = models.ForeignKey(SousCause , on_delete=models.CASCADE ,null=True)
    sousConsequance = models.ForeignKey(SousConsequance, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.descriptionCause


class Consequance(models.Model):
    descriptionConsequance = models.CharField(max_length=200)



class types (models.Model):
    type =models.CharField(max_length=200)

class Status (models.Model):
    status =models.CharField(max_length=200)


class Reclamations(models.Model):
    STATUS = (
        ('en cours', 'en cours'),
        ('ouvert', 'ouvert'),
        ('cloturer', 'cloturer')
    )

    SOURCES = (
        ('client', 'client'),
        ('fournisseur', 'fournisseur'),
        ('interne', 'interne')
    )
    TYPE = (
        ('Prix', 'Prix'),
        ('Qualité Produit', 'Qualité Produit'),
        ('Qualité Serice', 'Qualité Serice'),
        ('Modalité de Paiement', 'Modalité de Paiement'),
        ('Structure', 'Structure'),
        ('Délais', 'Délais'),

    )
    GRAVITY = (
        ('pas grave', 'pas grave'),
        ('moyen', 'moyen'),
        ('grave', 'grave'),
        ('trés grave', 'trés grave'),

    )

    PROBABILITY = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),

    )

    detecteurs = models.ForeignKey(Detecteur, on_delete=models.CASCADE,null=True)
    dateHeure_detection = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Date créationRec")
    sources = models.CharField(choices=SOURCES, default='client', max_length=100)
    nom_source = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    type = models.CharField(choices=TYPE, default='Prix', max_length=100)
    num_lots = models.IntegerField()
    num_cmd = models.IntegerField()
    quantite = models.CharField(max_length=60)
    probabiliter = models.CharField(choices=PROBABILITY, default='1', max_length=100)
    graviter = models.CharField(choices=GRAVITY, default='moyen', max_length=100)
    status = models.CharField(choices=STATUS, default='en cours', max_length=100)
    responsable_principale = models.ForeignKey(ResponsablePrincipal, on_delete=models.CASCADE, null=True)
    contribuer = models.ManyToManyField(Contribuer)
    informer = models.ForeignKey(Informer, on_delete=models.CASCADE, null=True)
    cause_rec = models.ForeignKey(Cause, on_delete=models.CASCADE, null=True)
    consequence_rec = models.ForeignKey(Consequance, on_delete=models.CASCADE, null=True)
    detector = models.CharField(max_length=40 ,null=True)
    statu = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    types = models.ForeignKey(types, on_delete=models.CASCADE, null=True)



class Risque(models.Model):
        STATUS = (
            ('en cours', 'en cours'),
            (' en attente', ' en attente'),
            ('clôturer ', 'clôturer ')
        )

        SOURCES = (
            ('client', 'client'),
            ('fournisseur', 'fournisseur'),
            ('interne', 'interne')
        )
        ISHIKAWA = (
            # milieu
            ('depot', 'depot'),
            ('usine', 'usine'),
            ('matiére', 'matiére'),
            ('main d oeuvre', 'main d oeuvre'),
            ('machine embalage', 'machine embalage'),
            ('batteur', 'batteur'),
            ('methode', 'methode'),

        )

        GRAVITY = (
            ('pas grave', 'pas grave'),
            ('moyen', 'moyen'),
            ('grave', 'grave'),
            ('trés grave', 'trés grave'),

        )
        PROBABILITY = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),

        )
            
        detector = models.CharField(max_length=40)
        dateHeure_detection = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Date création")
        sources = models.CharField(choices=SOURCES, default='interne', max_length=100)
        nom_source = models.CharField(max_length=40)
        description = models.CharField(max_length=100)
        ishikawa = models.CharField(choices=ISHIKAWA, default='methode', max_length=100)
        probabiliter = models.CharField(choices=PROBABILITY, default='1', max_length=100)
        graviter = models.CharField(choices=GRAVITY, default='grave', max_length=100)
        status = models.CharField(choices=STATUS, default='en attente', max_length=100)
        responsable_principale = models.ForeignKey(ResponsablePrincipal, on_delete=models.CASCADE, null=True)

        def __str__(self):
            return self.description

class CauseRell(models.Model):

    descriptionCauses = models.CharField(max_length=200)
    dateHeure_detection = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Dates création")


class ConsRell(models.Model):
    descriptionConsReel = models.CharField(max_length=200)
    dateHeure_detection = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Dates création")

class SousCauseRell(models.Model):

    descriptionSous_Causes = models.CharField(max_length=200)
    dateHeure_detection = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Datecréations")

class SousConsRell(models.Model):

    descriptionSous_Cons = models.CharField(max_length=200)
    dateHeure_detection = models.DateTimeField(default=timezone.now, blank=True, verbose_name="Dates_créations")
