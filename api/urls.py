from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'fields', views.FieldViewSet)
router.register(r'country', views.CountryViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'candidate', views.CandidateViewSet)
router.register(r'company', views.CompanyViewSet)
router.register(r'metier', views.MetierViewSet)
router.register(r'phone', views.PhoneViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'formation', views.FormationViewSet)
router.register(r'contrat', views.ContratViewSet)
router.register(r'offre', views.OffreViewSet)
router.register(r'competence', views.CompetenceViewSet)
router.register(r'langue', views.LangueViewSet)
router.register(r'document', views.DocumentViewSet)
router.register(r'application', views.ApplicationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url('login/', views.LoginView.as_view()),
    url('logout/', views.LogoutView.as_view()),
    # url(r'city/(?P<code>.+)/$', views.CityViewSet.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
