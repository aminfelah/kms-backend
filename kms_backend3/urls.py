from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView  )
from rest_framework.urlpatterns import format_suffix_patterns
#from django.conf import settings
from kms import views
#UserSerializer
urlpatterns = [
    path('kms/', include('kms.urls', namespace='kms')),#initialize the app
    path('kms/user/', include('kms.urls', namespace='kmss')),#user

    path('admin/', admin.site.urls),#admin
    path('kms-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('info', views.UserView.as_view()),  # user

    path('reclist/', views.ReclamationList.as_view()),  ##les listes des reclamations
    path('rec/', views.ReclamationForm.as_view()),  # la formulaire du  Reclmations a remplir par le  detecteur
    path('getrec/<int:id_r>', views.ReclamationFilledForm.as_view()),  # la Reclmations deja  remplit  qui s'affiche pour le Responsable pricipale
    #path('listrp/', views.ReclamationdesRp.as_view()),# description  de la reclamtion
    #path('listcon/', views.ReclamationdesCon.as_view()),#list description for con
    path('userinfo/', views.Userrec.as_view()),#la fonction et nom de l'utilisateurs
    #path('userDet/', views.UserDetector.as_view()),  # Detfun

    #path('rp/', views.RPList.as_view()),#Gestion Personne RP
    #path('contribuer/', views.ContribuerList.as_view()),#Gestion Personne contribuer
    #path('informer/', views.InformerList.as_view()),#Gestion Personne informer
    path('causereel/', views.CauseReelView.as_view()),#CauseReel ajouté par le responsable principale
    path('consreel/', views.ConsReelView.as_view()),#Consequence Reel ajouté par le responsable principale
    path('souscausereel/', views.SousCauseReelView.as_view()),#sousCauseReel ajouté par le contribiteur
    path('sousconsreel/', views.SousConsReelView.as_view()),#sousconsReel ajouté par le contribiteur
    path('causedes/', views.CauseListdes.as_view()),  # #catalogue cause
    #path('newcause/', views.NewCause.as_view()),#no
    path('consequence/', views.ConsequenceList.as_view()),#catalogue consequence
    path('souscons/', views.SousConseList.as_view()),#sous cons du catalogue
    path('souscause/', views.SousCauseList.as_view()),  # sous cause du catalogue
    path('taches/', views.TachesList.as_view()),#tabletache
    path('risques/', views.RisquesForm.as_view()),#Risques Formulaire




]
urlpatterns = format_suffix_patterns(urlpatterns)