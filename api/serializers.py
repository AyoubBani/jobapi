# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Candidate, Company, MyUser, Country, City, Secteur, Metier, Phone, Specialite, Experience, \
    Formation, Contrat, Offre, Competence, Langue, Document, Application
from django.contrib.auth import authenticate
from rest_framework import exceptions


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'


class LangueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langue
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    # country = CountrySerializer()

    class Meta:
        model = City
        fields = '__all__'


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'


class SecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secteur
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class MetierSerializer(serializers.ModelSerializer):
    secteur = SecteurSerializer()

    class Meta:
        model = Metier
        fields = '__all__'


class SpecialiteSerializer(serializers.ModelSerializer):
    metier = MetierSerializer(many=True)

    class Meta:
        model = Specialite
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    ville = CitySerializer()

    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'profile_image', 'ville', 'about')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        self.email = data.get("email", "")
        self.password = data.get("password", "")

        if self.email and self.password:
            user = authenticate(email=self.email, password=self.password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is desactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with the given credentials."
                exceptions.ValidationError(msg)
        else:
            msg = "Must provide email and password both"
            raise exceptions.ValidationError(msg)
        return data


class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    metier = SpecialiteSerializer()

    class Meta:
        model = Candidate
        fields = '__all__'
        # return Response({'detail': 'Candidate Registered Successfully: '})


'''
    def create(self, validated_data):
        field = Feild.objects.all().get(domaine=validated_data['domaine'])
        print('User setup')
        usr = MyUser.objects.create_user(email=validated_data['email'], password=validated_data['password'],
                                         first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        usr.is_candidate = True
        usr.save()
        print('User Saved')
        nat = Country.objects.get(code='UNK')
        cit = City.objects.get(country=nat)
        candidate = Candidate.objects.create(user=usr, domaine=field, nationalite=nat, residence=cit)
        candidate.save()
        print('Candidate Saved')

        # candidate = Candidate.objects.create_user(
        #     username    =validated_data['email'], # HERE
        #     email       =validated_data['email'],
        #     password    =validated_data['password'],
        #     first_name  =validated_data['first_name'],
        #     last_name   =validated_data['last_name'],
        #     avatar      =validated_data['avatar'],
        # )
        return candidate
'''

'''
    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user
'''


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'


class ContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = '__all__'


class OffreSerializer(serializers.ModelSerializer):
    contrat = ContratSerializer()
    company = CompanySerializer()
    metier = MetierSerializer()

    class Meta:
        model = Offre
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer()
    offer = OffreSerializer()
    attachement = DocumentSerializer(many=True)

    class Meta:
        model = Application
        fields = '__all__'
