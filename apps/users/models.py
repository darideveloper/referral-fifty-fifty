import secrets
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=False)
    hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return f"{self.name} {self.last_name}"
    
    def save (self, *args, **kwargs):
        
        if not self.hash:
            self.hash = secrets.token_hex(32)
            
        super().save(*args, **kwargs)
    
class Store (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__ (self):
        return self.name
    
class ReferralLink (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    
    def __str__ (self):
        return f"{self.user} - {self.store} ({self.link})"

class LoginCodes (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=64)
    datetime = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return f"{self.user} - {self.hash}"
    
    def save (self, *args, **kwargs):
        
        if not self.hash:
            self.hash = secrets.token_hex(32)
            
        super().save(*args, **kwargs)