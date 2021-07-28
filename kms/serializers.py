
from rest_framework import serializers
from .models import  User,Tache, Commande, Client, ResponsablePrincipal, Contribuer, Informer, SousCause, Cause, Consequance, \
    Reclamations, Risque,SousConsequance ,Detecteur, CauseRell , ConsRell, SousCauseRell , SousConsRell

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fonction', 'name', 'email', 'password' ,'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# les listes des reclamations
class ReclmationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reclamations
        fields = ['id','detector', 'dateHeure_detection', 'sources', 'nom_source', 'description', 'num_lots',
                  'num_cmd', 'quantite', 'status',
                  ]

        depth = 2

# la formulaire du  Reclmations a remplir par le  detecteur
class ReclmationsSerializerForm(serializers.ModelSerializer):
    class Meta:
        model = Reclamations
        fields = ['id', 'nom_source', 'description', 'num_lots','detector',
                  'num_cmd', 'quantite' ,'types', 'status']
        depth = 2

# la Reclmations deja  remplit  qui s'affiche pour le Responsable pricipale
class ReclmationsSerializerFilledForm(serializers.ModelSerializer):
    types = serializers.SlugRelatedField(read_only=True, slug_field='type')

    class Meta:
        model = Reclamations
        fields = ['id','detector', 'nom_source', 'description', 'num_lots','dateHeure_detection','responsable_principale',
                          'num_cmd', 'quantite', 'types','statu'
                         ,'probabiliter','graviter','informer', 'contribuer'
                 ]
        depth = 2
#list description for rp / con /informed
class ReclmationsSerializerdes(serializers.ModelSerializer):

    #responsable_principale = serializers.SlugRelatedField(read_only=True ,slug_field='Nom_prenomRp' )

    class Meta:

        model = Reclamations
        fields = ('id','description','responsable_principale', 'contribuer', 'type', )
        depth = 2

#la fonction et nom de l'utilisateurs
class userrecSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name' ,'fonction']


#tuser tache
class TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = ['nom_tache']


# sous cause du catalogue
class SousCauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCause
        fields = ['descriptionSousCause']
        depth = 1

class SousConsequanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousConsequance
        fields = ['descriptionSousCons']
        depth = 1
#catalogue cause
class CauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cause
        fields = [ 'descriptionCause' ,]

        depth = 2

class NewCauseSerializer(serializers.ModelSerializer):


    class Meta:
        model = Cause
        fields = ['ishikawa',  'contribuerC', 'descriptionCause']
        depth = 2

#catalogue consequence
class ConsequanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consequance
        fields = ['descriptionConsequance']
        depth = 1


class NewConseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consequance
        fields = ['descriptionConsequance']
        depth = 2

class RisquesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risque
        fields = ['id','detector',  'sources', 'nom_source', 'description' ]
        depth = 2





# Cause Reel ajouté par le responsable principale
class CauseReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CauseRell
        fields = ['id','descriptionCauses','dateHeure_detection' ]
        depth = 2

#Consequence Reel ajouté par le responsable principale
class ConsReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsRell
        fields = ['id','descriptionConsReel','dateHeure_detection' ]
        depth = 2
#sousCauseReel ajouté par le contribiteur
class SousCauseReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousCauseRell
        fields = ['id','descriptionSous_Causes','dateHeure_detection' ]
        depth = 2
#sousconsReel ajouté par le contribiteur
class SousConsReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SousConsRell
        fields = ['id','descriptionSous_Cons','dateHeure_detection' ]
        depth = 2