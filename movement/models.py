from django.db import models
from django.utils import timezone
# Create your models here.


class Movement(models.Model):
    movement_time=models.DateTimeField(null=False,blank=True)
    time=models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        
        if not self.movement_time:
            self.movement_time=timezone.localtime()
        return super().save(*args, **kwargs)