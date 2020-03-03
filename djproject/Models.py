from django.db import models
class User(models.Model):
    username= models.CharField(max_length=20)
    password= models.CharField(max_length=20)
    center= models.CharField(max_length=30)
    project= models.CharField(max_length=30)