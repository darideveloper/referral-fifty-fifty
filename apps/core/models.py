from django.db import models

class Token (models.Model):
  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        
    def __str__ (self):
        return self.token