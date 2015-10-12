# django2fa
Welcome to django2fa. An implementation of simple two factor authentication in django.

**INSTALLATION**

```python
pip install –r requierments.txt
```

**SMS**

You need a twilio account to get the sms working. You will also need to verify the numbers that twilio will be sending the texts too. You can send texts to unverified numbers if you upgrade to the paid options then finally you will have tp enter is your twilio access key and auth token at django2fa/settings.py

**Email**

You will also need SMTP settings for your email provider. Enter those at django/settings.py

**DIRECTORY STRUCTURE**

-Accounts/ - handles sign in, sign up and sign out actions
-Verification/ - handles all verification methods i.e. phone and email
-Dashboard/- after successful authentication the user is redirected to dashboard

**TO DO**

Improve on error handling (make it more friendly)

In case of any questions/problems.  Just start a new issue.
