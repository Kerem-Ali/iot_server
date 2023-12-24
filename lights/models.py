from django.db import models
from datetime import datetime
from django.utils.timezone import now

class Light(models.Model):
    name = models.CharField(max_length=50,unique=True)
    ip = models.CharField(max_length=100)
    is_on = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    creation_date = models.DateTimeField(default=now())
    last_communication_date = models.DateTimeField(default=now())
    
    def __str__(self):
        return f"{self.name}"
    
    
    

