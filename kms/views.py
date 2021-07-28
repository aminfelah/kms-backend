

from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from kms.serializers import UserSerializer
from .models import User
import jwt, datetime
from .models import Reclamations, User, Tache, Commande, ResponsablePrincipal,Contribuer, Informer, Cause,Consequance ,SousCause,SousConsequance, Detecteur,Risque, CauseRell, ConsRell ,SousConsRell ,SousCauseRell
from .serializers import  TacheSerializer,userrecSerializer,ReclmationsSerializer,  \
 CauseSerializer, SousCauseSerializer,ConsequanceSerializer,SousConsequanceSerializer,ReclmationsSerializerForm ,RisquesSerializer ,ReclmationsSerializerFilledForm , CauseReelSerializer ,ConsReelSerializer,SousCauseReelSerializer,SousConsReelSerializer
from rest_framework import serializers
from datetime import date #
from django.http import Http404

from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from django.db.models import F

# inscrition de l'utilisateur

class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# login de l'utilisateur
class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()


        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'email':user.email,
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# deconnexion de l'utilisateur
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response

# les listes des reclamations
class ReclamationList(APIView):
    """ Reclamation  """
    def get(self, request):

        rec = Reclamations.objects.all()
        serializer =ReclmationsSerializer(rec, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer =ReclmationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# la formulaire du  Reclmations a remplir par le  detecteur
class ReclamationForm(APIView):
    """ supports Reclamation which will be  filled"""

    def get(self, request):
        rec= Reclamations.objects.all()

        serializer = ReclmationsSerializerForm(rec, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer =ReclmationsSerializerForm(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# la Reclmations deja  remplit  qui s'affiche pour le Responsable pricipale
class ReclamationFilledForm(APIView):

    def get(self, request ,id_r):
        rec= Reclamations.objects.filter(id=id_r)
        serializer = ReclmationsSerializerFilledForm(rec, many=True)
        return Response(serializer.data)

#la fonction et nom de l'utilisateurs
class Userrec(APIView):

    """ users name  """
    def get(self, request):
        name =User.objects.all()
        serializer =userrecSerializer(name, many=True)
        return Response(serializer.data)
#All cause content

class CauseList(APIView):

    def get(self, request,  format=None):
       # snippet = self.get_object(pk)
        c =Cause.objects.all()
        serializer = CauseSerializer(c)
        return Response(serializer.data)

    def post(self, request):

        serializer = CauseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#catalogue cause
class CauseListdes(APIView):

    def get(self, request):

        cons= Cause.objects.all()

        serializer =CauseSerializer(cons, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs):
        serializer =  CauseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Cause Reel ajouté par le responsable principale
class CauseReelView(APIView):

    def get(self, request):
        cause = CauseRell.objects.all()
        serializer =CauseReelSerializer(cause, many=True)
        return Response(serializer.data)

    def post(self, request, format=None, *args, **kwargs):
        serializer = CauseReelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# sous cause du catalogue
class SousCauseList(APIView):
    def get(self, request, format=None):

        s_con_des =SousCause.objects.all()
        s_c= SousCauseSerializer(s_con_des, many=True)
        return Response(s_c.data)

    def post(self, request):
        serializer = SousCauseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#catalogue consequence
class ConsequenceList(APIView):
    def get(self, request, format=None):
        cons = Consequance.objects.all()
        serializer = ConsequanceSerializer(cons, many=True)
        return Response(serializer.data)


def post(self, request, format=None, *args, **kwargs):
    # uv = Consequance(descriptionConsequance=self.request.cons)
    serializer = ConsequanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#sous cons du catalogue
class SousConseList(APIView):
    def get(self, request, format=None):

        s_con_des =SousConsequance.objects.all()
        s_c= SousConsequanceSerializer(s_con_des, many=True)
        return Response(s_c.data)

    def post(self, request):
        serializer = SousConsequanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#user tache
class TachesList(APIView):

    def get(self, request, format=None):
        tache = Tache.objects.all()
        serializer = TacheSerializer(tache, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = TacheSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RisquesForm(APIView):

    def get(self, request):
        rec= Risque.objects.all()
        serializer = RisquesSerializer(rec, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer =RisquesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Consequence Reel ajouté par le responsable principale
class ConsReelView(APIView):

    def get(self, request, format=None):

        consreel =ConsRell.objects.all()
        cons= ConsReelSerializer(consreel, many=True)
        return Response(cons.data)

    def post(self, request):
        serializer = ConsReelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#sousCauseReel ajouté par le contribiteur
class SousCauseReelView(APIView):

    def get(self, request, format=None):

        S_cause =SousCauseRell.objects.all()
        cons= SousCauseReelSerializer(S_cause, many=True)
        return Response(cons.data)

    def post(self, request):
        serializer = SousCauseReelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#sousconsReel ajouté par le contribiteur
class SousConsReelView(APIView):

    def get(self, request, format=None):

        cons = SousConsRell.objects.all()
        cons1= SousConsReelSerializer(cons, many=True)
        return Response(cons1.data)

    def post(self, request):
        serializer = SousConsReelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)