from zoneinfo import ZoneInfo

import pytz
from django.db import models
from django.utils import timezone
from store.models import Product

from siteLariParis.settings import AUTH_USER_MODEL


class Article(models.Model):
    """ Article :  une ligne du panier."""
    #user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.00)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return(f"{self.product.name} x {self.quantity}")
    
    def compute_sub_total_price(self):
        self.price = self.product.price * self.quantity
        return(self.product.price * self.quantity)

class Cart(models.Model):
    #def __init__(self, request):
    #    self.session = request.session
    #articles = models.ForeignKey(Article, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)
    total_price = models.FloatField(default=0.00)
    tax = models.FloatField(default=0.20)
    delivery_price = models.FloatField(default=0.00)
    quantity_total = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return(f"{self.quantity_total} articles pour {self.total_price}")
    
    #def delete(self, *args, **kwargs):
    #    self.articles.clear()
    #    super().delete(*args, **kwargs)

    def compute_total_price(self):
        pr=0.0
        for article in self.articles.all():
            pr += article.product.price * article.quantity
        self.total_price = pr + self.delivery_price
        return(pr)
    
    def compute_total_quantity(self):
        qt=0
        for article in self.articles.all():
            qt += article.quantity
        self.quantity_total = qt
        return(qt)
    
    def update_cart_instance(self):
        self.total_price = self.compute_total_price()
        self.quantity_total = self.compute_total_quantity()
        
class Delivery(models.Model):
    firstname = models.CharField(max_length=70, null=False, blank=False)
    lastname = models.CharField(max_length=70, null=False, blank=False)
    phone_number = models.IntegerField(null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    Adresse = models.CharField(max_length=150, null=False, blank=False)
    adresse_complementaire = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=40, null=False, blank=False)
    Ville = models.CharField(max_length=60, null=False, blank=False)
    zip_code = models.IntegerField(null=False, blank=False)

class userDeliveryAdress(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
    delivery_adress = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)


class STATUS_ORDER(models.TextChoices):
    NON_PAYE = "PAIEMENT NON validé"
    PAIEMENT_VALIDE = "PAIEMENT validé"
    EXPEDIE = "EXPEDITION EN COURS"
    LIVRE  = "COMMANDE LIVREE"
    ANNULEE = "COMMANDE Annulée"


class ClassicOrder(models.Model):
    """ Commandes faites par un utilisateur authentifié
    """
    #order_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete = models.CASCADE)
    #cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)
    delivery_address = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)
    #payment =
    ordered  = models.BooleanField(default=False) # payment done ? yes | no
    ordered_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUS_ORDER.choices, default=STATUS_ORDER.NON_PAYE, max_length=25, null=False, )
    tax = models.FloatField(default=0.20)
    delivery_price = models.FloatField(default=0.00)

    def __str__(self):
        return(f"{self.user.last_name} {self.user.first_name} \n statut : {self.status}")
    
    def place_order(self):
        timezone_paris = pytz.timezone('Europe/Paris')
        self.ordered = True
        self.ordered_date= timezone.now().astimezone(timezone_paris)
        for article in self.articles.all():
            article.ordered = True
            article.ordered_date = timezone.now().astimezone(timezone_paris)
            article.save()
        self.save()

    def compute_total_price(self):
        pr=0.0
        for article in self.articles.all():
            pr += article.product.price * article.quantity
        pr += self.delivery_price
        self.total_price = pr
        return(pr)
    
    def compute_total_quantity(self):
        qt=0
        for article in self.articles.all():
            qt += article.quantity
        self.quantity_total = qt
        return(qt)
    
    def update(self):
        self.total_price = self.compute_total_price()
        self.quantity_total = self.compute_total_quantity()
    
class AnonymousOrder(models.Model):
    """ commandes faites par un utilisateur anonyme"""
    #order_number = models.CharField(max_length=100, unique=True)
    articles = models.ManyToManyField(Article)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)
    ordered  = models.BooleanField(default=False) # payment done ? yes | no
    ordered_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=STATUS_ORDER.choices, max_length=25, null=False, )
    tax = models.FloatField(default=0.20)
    delivery_price = models.FloatField(default=0.00)

    def __str__(self):
        return(f"{self.cart.total_price} € for {self.cart.quantity_total} products")
    
    def place_order(self):
        timezone_paris = pytz.timezone('Europe/Paris')
        self.ordered = True
        self.ordered_date= timezone.now().astimezone(timezone_paris)
        for article in self.articles.all():
            article.ordered = True
            article.ordered_date = timezone.now().astimezone(timezone_paris)
            article.save()
        self.save()

    def compute_total_price(self):
        pr=0.0
        for article in self.articles.all():
            pr += article.product.price * article.quantity
        self.total_price = pr
        return(pr)
    
    def compute_total_quantity(self):
        qt=0
        for article in self.articles.all():
            qt += article.quantity
        self.quantity_total = qt
        return(qt)
    
    def update(self):
        self.total_price = self.compute_total_price()
        self.quantity_total = self.compute_total_quantity()
    