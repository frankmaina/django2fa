from django.db import models
from django.contrib.auth.models import User


class PhoneVerification(models.Model):
	user = models.ForeignKey(User)
	action = models.CharField(max_length=25)
	phone_number = models.CharField(max_length=25)
	code = models.IntegerField()
	active = models.BooleanField()
	verified = models.BooleanField()


class EmailVerification(models.Model):
	user = models.ForeignKey(User)
	email_token = models.CharField(max_length=32)
	active = models.BooleanField()
	verified = models.BooleanField()