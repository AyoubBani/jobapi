from _elementtree import ParseError
from decimal import Decimal

from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import Candidate, Company, MyUser, Country, City, Metier, Specialite, Phone, Experience, Formation, \
    Contrat, Offre, Competence, Langue, Document, Application
from .serializers import CandidateSerializer, UserSerializer, LoginSerializer, CountrySerializer, \
    CitySerializer, CompanySerializer, MetierSerializer, PhoneSerializer, ExperienceSerializer, FormationSerializer, \
    ContratSerializer, OffreSerializer, CompetenceSerializer, LangueSerializer, DocumentSerializer, \
    ApplicationSerializer
from django.contrib.auth import login as django_login, logout as django_logout
import json


def get_custom_user_response(user, type):
    token, created = Token.objects.get_or_create(user=user)
    if type is 'candidate':
        cnd = Candidate.objects.all().get(user=user)
        candidate = {
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_image": 'http://127.0.0.1:8000/media/' + user.profile_image.name,
                "ville": {
                    "id": user.ville.id,
                    "name": user.ville.name,
                    "country": user.ville.country.code
                },
                "about": user.about
            },
            "metier": {
                "id": cnd.metier.id,
                "metier": [
                    {
                        "id": cnd.metier.metier.get().id,
                        "secteur": {
                            "id": cnd.metier.metier.get().secteur.id,
                            "secteur": cnd.metier.metier.get().secteur.secteur
                        },
                        "metier": cnd.metier.metier.get().metier
                    }
                ],
                "experience": cnd.metier.experience
            },
            "birthdate": cnd.birthdate,
            "etat_civil": cnd.etat_civil
        }
        return Response({"token": token.key, "type": type, type: candidate}, status=200)
    else:
        cnd = Company.objects.all().get(user=user)
        company = {
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_image": 'http://127.0.0.1:8000/media/' + user.profile_image.name,
                "ville": {
                    "id": user.ville.id,
                    "name": user.ville.name,
                    "country": user.ville.country.code
                },
                "about": user.about
            },
            "company_name": cnd.company_name,
            "description": cnd.description,
            "website": cnd.website
        }
        return Response({"token": token.key, "type": type, type: company}, status=200)
    # print(candidate)
    # print('dumping...')
    # print(print(json.dumps(candidate)))


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }

        return Response(content)

    def post(self, request):
        print('Login ... ')
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        type = 'candidate' if user.is_candidate else 'company'
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return get_custom_user_response(user, type)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        django_logout(request)
        return Response(status=204)


#
# class FieldViewSet(viewsets.ModelViewSet):
# queryset = Feild.objects.all().filter(~Q(domaine=''))
#     serializer_class = FeildSerializer


class CountryViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Country.objects.all().order_by('name')
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = City.objects.all().order_by("name")
    serializer_class = CitySerializer

    '''
    def get_queryset(self):
        # req = self.request
        code = self.kwargs['code']
        country = Country.objects.all().get(code=code)
        print('Getting cities of ' + country.name)
        self.queryset = City.objects.filter(country=country).order_by('name')
        print('cities')
        print(self.queryset)
        return self.queryset
    '''


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


def fexperience(x):
    return {
        2: 'Moins de 1 an',
        3: 'De 1 à 3 ans',
        4: 'De 3 à 5 ans',
        5: 'De 5 à 10 ans',
        6: 'De 10 à 20 ans',
        7: 'Plus de 20 ans',
    }.get(x, 'Débutant')


class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        competence = request.data.get('competence')
        niveau = request.data.get('niveau')
        candidate = Candidate.objects.all().get(user=self.request.user)
        competence = Competence(competence=competence, niveau=int(niveau), user=candidate)
        competence.save()
        return Response({'detail': 'Competence Created Successfully'})


class LangueViewSet(viewsets.ModelViewSet):
    queryset = Langue.objects.all()
    serializer_class = LangueSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        langue = request.data.get('langue')
        niveau = request.data.get('niveau')
        candidate = Candidate.objects.all().get(user=self.request.user)
        competence = Langue(langue=langue, niveau=int(niveau), user=candidate)
        competence.save()
        return Response({'detail': 'Langue Created Successfully'})


class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Phone.objects.all().filter(user=self.request.user)
        # return self.request.user.accounts.all()

    def create(self, request, *args, **kwargs):
        code = request.data.get('code')
        number = request.data.get('number')
        phone = Phone(code=code, number=number, user=request.user)
        phone.save()
        return Response({'detail': 'Phone Added Successfully'})

    # def update(self, request, *args, **kwargs):
    #     phone = Phone.objects.all().get(user=request.user)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        candidate = Candidate.objects.all().get(user=self.request.user)
        return Experience.objects.all().filter(user=candidate)

    def create(self, request, *args, **kwargs):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        intitule = request.data.get('intitule')
        description = request.data.get('description')
        # phone = Phone(code=code, number=number, user=request.user)
        candidate = Candidate.objects.all().get(user=self.request.user)
        experience = Experience(user=candidate, start_date=start_date, end_date=end_date, intitule=intitule,
                                description=description)
        experience.save()
        return Response({'detail': 'Experience Added Successfully'})


class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        candidate = Candidate.objects.all().get(user=self.request.user)
        return Formation.objects.all().filter(user=candidate)

    def create(self, request, *args, **kwargs):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        institute = request.data.get('institute')
        diplome = request.data.get('diplome')
        # phone = Phone(code=code, number=number, user=request.user)
        candidate = Candidate.objects.all().get(user=self.request.user)
        formation = Formation(user=candidate, start_date=start_date, end_date=end_date, institute=institute,
                              diplome=diplome)
        formation.save()
        return Response({'detail': 'Formation Added Successfully'})


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        print('New Candidate Registration')
        email = request._request.POST.get('email')
        print('email is: ' + email)
        try:
            file = request._request.FILES['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        metier = request.POST.get('metier')
        id = request.POST.get('experience')
        ville = request.POST.get('ville')
        city = City.objects.all().get(id=int(ville))
        met = Metier.objects.all().get(metier=metier)
        sp = Specialite(experience=fexperience(int(id)))
        sp.save()
        sp.metier.add(met)
        user = MyUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name,
                                          ville=city, prf_image=file)
        user.is_candidate = True
        user.save()
        candidate = Candidate.objects.create(user=user, metier=sp)
        candidate.save()
        return Response({'detail': 'Candidate Created Successfully'})

    def update(self, request, *args, **kwargs):
        print('Update Candidate ', request.data.get('user').get('id'))
        print(request.data)
        user = MyUser.objects.all().get(id=request.data.get('user').get('id'))
        candidate = Candidate.objects.all().get(user=user)
        # print('BIRTHDATE')
        # print(request.data.get('birthdate'))
        # print('etat_civil')
        # print(request.data.get('etat_civil'))
        if request.data.get('birthdate') is not None:
            print(request.data.get('birthdate'))
            candidate.birthdate = request.data.get('birthdate')
        if request.data.get('etat_civil') is not None:
            print(request.data.get('etat_civil'))
            candidate.etat_civil = request.data.get('etat_civil')
        if request.data.get('about') != '':
            print(request.data.get('user').get('about'))
            candidate.user.about = request.data.get('user').get('about')
        candidate.user.save()
        candidate.save()
        return get_custom_user_response(user, 'candidate')
        # return Response({'detail': 'Candidate Created Successfully'})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        print('New Company Registration')
        email = request._request.POST.get('email')
        print('email is: ' + email)
        try:
            file = request._request.FILES['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        # product = Product.objects.create(image=file, ....)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        ville = request.POST.get('ville')
        company_name = request.POST.get('company_name')
        website = request.POST.get('website')
        city = City.objects.all().get(id=int(ville))
        user = MyUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name,
                                          ville=city, prf_image=file)
        user.is_company = True
        user.save()
        company = Company.objects.create(user=user, company_name=company_name, website=website)
        company.save()
        return Response({'detail': 'Company Created Successfully'})


class MetierViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Metier.objects.all().order_by("secteur")
    serializer_class = MetierSerializer


class ContratViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        if self.request.user.is_company:
            company = Company.objects.all().get(user=self.request.user)
            offers = Offre.objects.all().filter(company=company)
            return Application.objects.all().filter(offer__in=offers)
        else:
            candidate = Candidate.objects.all().get(user=self.request.user)
            return Application.objects.all().filter(candidate=candidate)

    def create(self, request, *args, **kwargs):
        print('New Application')
        # print(request.data)
        lettre_motivation = request.data.get('lettre_motivation')
        offer = Offre.objects.all().get(id=request.data.get('offer').get('id'))
        print('Offre')
        print(offer)
        candidate = Candidate.objects.all().get(user=self.request.user)
        app = Application(candidate=candidate, offer=offer, lettre_motivation=lettre_motivation)
        app.save()
        for att in request.data.get('attachement'):
            doc = Document.objects.all().get(nom=att['nom'])
            app.attachement.add(doc)
        return Response({'detail': 'Application Created Successfully'})


class OffreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Offre.objects.all()
    serializer_class = OffreSerializer

    def get_queryset(self):
        # candidate = Candidate.objects.all().get(user=self.request.user)
        # return Experience.objects.all().filter(user=candidate)
        if self.request.user.is_candidate:
            print('Candidate get all')
            return Offre.objects.all()
        else:
            print('Company Get Only mine')
            company = Company.objects.all().get(user=self.request.user)
            return Offre.objects.all().filter(company=company)

    def create(self, request, *args, **kwargs):
        print('REQUEST NEW OFFRE DATA: ')
        print(request.data)
        # titre = request._request.POST.get('titre')
        print('Contrat')
        print(request.data.get('contrat'))
        contrat = request.data.get('contrat').get('contrat')
        company = request.data.get('company').get('user').get('id')
        metier = request.data.get('metier').get('metier')
        description = request.data.get('description')
        salaire = request.data.get('salaire')
        titre = request.data.get('titre')

        myContrat = Contrat.objects.all().get(id=int(contrat))
        user = MyUser.objects.all().get(id=company)
        myCompany = Company.objects.all().get(user=user)
        met = Metier.objects.all().get(metier=metier)

        offre = Offre.objects.create(titre=titre, contrat=myContrat, company=myCompany, metier=met,
                                     description=description, salaire=Decimal(salaire))
        offre.save()
        # print('REQUEST NEW OFFRE DATA: ')
        # print(request.data)
        # print(request.data.get('titre'))
        return Response({'detail': 'Offre Created Successfully'})


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        candidate = Candidate.objects.all().get(user=self.request.user)
        return Document.objects.all().filter(user=candidate)
        # return self.request.user.accounts.all()

    def create(self, request, *args, **kwargs):
        nom = request._request.POST.get('nom')
        try:
            document = request._request.FILES['document']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        candidate = Candidate.objects.all().get(user=self.request.user)
        document = Document(nom=nom, document=document, user=candidate)
        document.save()
        return Response({'detail': 'Document Added Successfully'})

    def destroy(self, request, pk=None):
        document = Document.objects.all().get(pk=pk)
        document.document.delete()
        document.delete()
        return Response({'detail': 'Document Removed Successfully'})
