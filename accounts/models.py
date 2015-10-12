from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
    
class UserProfile(models.Model):
	user = models.ForeignKey(User)
	phone_number = models.IntegerField()