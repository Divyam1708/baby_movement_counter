from django.db import models

# Create your models here.


class Movement(models.Model):
    time=models.DateTimeField(auto_now_add=True)