from django.contrib import admin
from store.models import Categorie, Finition, Lace, Product, Taille

# Register your models here.

admin.site.register(Categorie)
admin.site.register(Finition)
admin.site.register(Lace)
admin.site.register(Taille)

class ProductAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('name', 'categorie','price') # liste les champs que nous voulons sur l'affichage de la liste

admin.site.register(Product, ProductAdmin)

