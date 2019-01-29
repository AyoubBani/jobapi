import os

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models import ImageField


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


def get_file_path(instance, filename):
    return os.path.join('files', str(instance.user.user.email), filename)


class Country(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=120, unique=True, null=False)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=120, unique=True, null=False)

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, ville=None, prf_image=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if ville is None:
            ville = City.objects.all().get(id=1)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            ville=ville
        )

        user.set_password(password)
        # user.domaine = domaine
        user.profile_image = prf_image
        user.ville = ville
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# class Feild(models.Model):
#     domaine = models.CharField(max_length=170, unique=True, null=False)
#     def __str__(self):
#         return self.domaine


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    profile_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    # domaine = models.ForeignKey(Feild, related_name='dom_cand', on_delete=models.CASCADE)
    ville = models.ForeignKey(City, related_name='residence', on_delete=models.CASCADE)
    # date_of_birth = models.DateField()
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    about = models.TextField(max_length=900, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # 'profile_image', 'domaine'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# DEFAULT_COUNTRY_ID = Country.objects.get(code='UNK').code


class Secteur(models.Model):
    secteur = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.secteur


class Metier(models.Model):
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    metier = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.metier


class Specialite(models.Model):
    metier = models.ManyToManyField(Metier)
    experience = models.CharField(max_length=120, default='Debutant')

    def __str__(self):
        return 'Travaille sur ' + self.metier.get().metier + ' experience ' + self.experience


class Candidate(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    birthdate = models.DateField(null=True)
    etat_civil = models.CharField(max_length=80, null=True, unique=False)
    # null = True
    # phone = models.ForeignKey(Phone, related_name='phone_number', on_delete=models.CASCADE)
    # metier = models.ForeignKey(Metier, related_name='metier_candidat', on_delete=models.DO_NOTHING)
    metier = models.ForeignKey(Specialite, related_name='metier_candidat', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.email

    '''
    def save(self, *args, **kwargs):
        if not self.residenceCountry:
            self.residenceCountry = self.nationalite
        super().save(*args, **kwargs)
    '''


class Company(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=800, default='')
    website = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.user.email


class Phone(models.Model):
    code = models.CharField(max_length=3)
    number = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(MyUser, related_name='phone_number', on_delete=models.CASCADE)

    def __str__(self):
        return self.number


class Document(models.Model):
    # user = models.OneToOneField(Candidate, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(Candidate, related_name='user_document', on_delete=models.CASCADE)
    nom = models.CharField(max_length=120, null=False)
    # type = models.CharField(max_length=120, null=False)
    document = models.FileField(db_index=True, upload_to=get_file_path)

    def __str__(self):
        return self.nom


class Competence(models.Model):
    # user = models.OneToOneField(Candidate, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(Candidate, related_name='user_competence', on_delete=models.CASCADE)
    competence = models.CharField(max_length=120, null=False)
    niveau = models.IntegerField(max_length=3, null=False)

    def __str__(self):
        return self.competence


class Langue(models.Model):
    user = models.ForeignKey(Candidate, related_name='user_langue', on_delete=models.CASCADE)
    langue = models.CharField(max_length=120, null=False)
    niveau = models.IntegerField(max_length=3, null=False)

    def __str__(self):
        return self.langue


class Experience(models.Model):
    # user = models.OneToOneField(Candidate, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(Candidate, related_name='user_experience', on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    intitule = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=900, null=True)

    def __str__(self):
        return self.intitule


class Formation(models.Model):
    # user = models.OneToOneField(Candidate, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(Candidate, related_name='user_formation', on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    institute = models.CharField(max_length=120, null=False)
    diplome = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.institute + ' ' + self.diplome


class Contrat(models.Model):
    contrat = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.contrat


class Offre(models.Model):
    titre = models.CharField(max_length=120, default='')
    contrat = models.ForeignKey(Contrat, related_name='contrat_offre', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='company_offre', on_delete=models.CASCADE)
    metier = models.ForeignKey(Metier, related_name='metier_offre', on_delete=models.CASCADE)
    description = models.TextField(null=False)
    salaire = models.DecimalField(max_digits=12, decimal_places=2)
    etat = models.CharField(max_length=50, default='active')

    def __str__(self):
        return self.titre


class Application(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='candidate_application', on_delete=models.CASCADE)
    offer = models.ForeignKey(Offre, related_name='offer_application', on_delete=models.CASCADE)
    attachement = models.ManyToManyField(Document)
    lettre_motivation = models.TextField(null=False)

    def __str__(self):
        return self.candidate.user.first_name + ' postuler a ' + self.offer.titre
