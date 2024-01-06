from django.contrib.auth.models import AbstractUser, AnonymousUser

# Create your models here.

class Shopper(AbstractUser) :
    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
"""class Customer(models.Model):
    lastname = models.CharField(max_length= 60, null=False, blank=False)
    firstname = models.CharField(max_length = 50, null=False, blank=False)
    telephone = models.IntegerField(default = 1234567890, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    prefix_phone = models.IntegerField(default = 33, null=False, blank=False)
    adresse = models.CharField(max_length= 150, null=False, blank=False)
    code_postal = models.IntegerField(default = 75015, null=False, blank=False)
    ville = models.CharField(max_length= 60, null=False, blank=False)
    pays = models.CharField(max_length= 50, null=False, blank=False)

    def __str__(self):
        return f'{self.lastname + " " + self.firstname}'
"""