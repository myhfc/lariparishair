# Create your models here.
from django.db import models
from django.utils.text import slugify

#from django.urls import reverse


class Categorie(models.Model):
    name = models.fields.CharField(max_length=16, null=True, blank=False)
    slug = models.fields.SlugField(default='perruques',max_length=16, null=True,blank=False)
    image_categorie = models.ImageField(upload_to="products/categories", null=True)
    image_categorie1 = models.ImageField(upload_to="products/categories", null=True)
    def __str__(self):
        return f'{self.name}'
    
class Finition(models.Model):
    name = models.fields.CharField(max_length=16, null=True, blank=False)
    def __str__(self):
        return f'{self.name}'

class Lace(models.Model):
    name = models.fields.CharField(max_length=16, null=True, blank=False)
    def __str__(self):
        return f'{self.name}'
    
class Taille(models.Model):
    name = models.fields.CharField(max_length=16, null=True, blank=False)
    def __str__(self):
        return f'{self.name}'
    
class Texture(models.Model):
    name = models.fields.CharField(max_length=16, null=True, blank=False)
    def __str__(self):
        return f'{self.name}'

class PerruqueSousCategorie(models.Model):
    name = models.fields.CharField(max_length=20, null=True, blank=False)
    slug_name = models.fields.SlugField(unique=True, default = " ")#slugify(name))
    def __str__(self):
        return f'{self.name}'
    
class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.FloatField(default=200.0)
    stock = models.IntegerField(default=0)
    categorie = models.ForeignKey(Categorie, null=True, on_delete=models.SET_NULL)
    sous_categorie_perruque = models.ForeignKey(PerruqueSousCategorie, null=True, on_delete=models.SET_NULL) #models.CharField(choices=SousCategoriePerruque.choices, max_length=25, null=True, blank=True)
    short_description1 = models.CharField(max_length=50)
    short_description2 = models.CharField(max_length=50)
    description = models.TextField(blank=False, null=False)
    taille = models.ForeignKey(Taille, null=True, on_delete=models.SET_NULL)
    finition = models.ForeignKey(Finition, null=True, blank=True, on_delete=models.SET_NULL)
    choix_lace = models.ForeignKey(Lace, null=True, blank=True, on_delete=models.SET_NULL)
    image1 = models.ImageField(upload_to="products", null=True)
    image2 = models.ImageField(upload_to="products", null=True)

    def __str__(self):
        return f'{self.name}'
    
    def get_price(self):
        return self.price
    
    """def get_absolute_url(self, product_id=7):
        reverse("product_detail",kwargs={'product_id':product_id})
    """

class Images_site_lariparis(models.Model):
    name = models.CharField(max_length= 20, null=False, blank=False)
    image1_accueil_hero = models.ImageField(upload_to="accueil", null=True)
    image2_accueil_hero = models.ImageField(upload_to="accueil", null=True)
    
    def __str__(self):
        return f'{self.name}'
    







