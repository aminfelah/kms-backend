from django.contrib import admin
from kms.models import User
from django.contrib.auth.admin import UserAdmin
from kms.models import  Reclamations,  Client, Tache,  ResponsablePrincipal, Contribuer, Informer, \
    Commande, Cause, SousConsequance, SousCause, Consequance ,Detecteur, Risque ,CauseRell, ConsRell,SousCauseRell ,SousConsRell ,Status,types

admin.site.register(Reclamations)
admin.site.register(Client)
admin.site.register(Tache )
admin.site.register(ResponsablePrincipal)
admin.site.register(Contribuer)
admin.site.register(Informer)
admin.site.register(Risque)
admin.site.register(ConsRell)
admin.site.register(SousCauseRell)
admin.site.register(SousConsRell)
admin.site.register(CauseRell)
admin.site.register(Cause)
admin.site.register(SousConsequance)
admin.site.register(Commande)
admin.site.register(SousCause)
admin.site.register( Consequance)
#admin.site.register(tacheuser)
admin.site.register(Detecteur)
# control sur les utilisateur pour ajouté
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email','password' ,'fonction')
    list_filter = ('email','password','is_active', 'is_staff')

    list_display = ('email','password','fonction',
                    'is_active', 'is_staff')
    ordering = ('email',)



    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )

    add_fieldsets = UserAdmin.add_fieldsets =(
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','password1','password2','fonction','date_naissance','is_staff', 'is_active')}
         ),
    )

admin.site.register(User, UserAdminConfig)