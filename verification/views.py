from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import VerificationCodeForm
from twilio.rest import TwilioRestClient
from django.http import HttpResponseRedirect, HttpResponse
from django2fa.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
import random
import base64
from .models import PhoneVerification, EmailVerification
from accounts.models import UserProfile
from accounts.forms import signinform, signupform
from django.contrib.auth.models import User
from django.contrib.auth import logout


# sms sending function
def send_sms(code, phone_number):
    account = TWILIO_ACCOUNT_SID
    token = TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account, token)

    message = client.messages.create(to="+" + str(phone_number), from_=TWILIO_PHONE_NUMBER,
                                     body="Your verification code is: " + str(code))


@login_required(login_url='/accounts/signin/')
def index(request):
    # we first get all user data
    user = request.user
    profile = UserProfile.objects.get(user=user)
    phone_number = profile.phone_number
    if request.method == 'POST':
        # then process the code that was submitted
        code = request.POST['code']
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            # process code
            verification_session = PhoneVerification.objects.get(
                user=user, active=1, verified=0)
            if str(code) == str(verification_session.code):
                # the code passed hence ther verification request is not active
                # but is verified
                verification_session.active = 0
                verification_session.verified = 1
                verification_session.save()
                return render(request, 'verification/success.html', {'user': user})
            else:
                # the code failed hence ther verification request is not active
                # and also not verified
                verification_session.active = 0
                verification_session.verified = 0
                verification_session.save()
                # we logout the user so that he/she would have to submit
                # another phone verification request
                logout(request)
                return render(request, 'verification/failed.html', {'user': user})
        else:
            # the form had an error hence not activated or verified
            verification_session.active = 0
            verification_session.verified = 0
            verification_session.save()
            # we logout the user due to incorrect details
            logout(request)
            return HttpResponse(form)
    else:
        # this is a GET request so we process a new Phone verification request
        code = random.randint(1000, 9999)
        verification = PhoneVerification.objects.create(
            user=user,
            action='verify',
            phone_number=phone_number,
            code=code,
            active=1,
            verified=0
        )
        try:
            send_sms(code, phone_number)
        except Exception as e:
            # sms reuest failed so cancel everything
            verification.active = 0
            verification.verified = 0
            verification.save()
            logout(request)
            return HttpResponse("An error occurred, probably with your network connection. You have been logged out,pleasew log back in to try again.")
        form = VerificationCodeForm()
        return render(request, 'verification/index.html', {'user': user, 'form': form})


def email_verification(request):
    if request.GET['token']:
        token = base64.b64decode(request.GET['token'])
        token = str(token)
        try:
            email_verification = EmailVerification.objects.get(
                email_token=token, active=1, verified=0)
            form = signinform()
            email_verification.active = 0
            email_verification.verified = 1
            email_verification.save()
            user = User.objects.get(id=email_verification.user.id)
            user.is_active = 1
            user.save()
            # do not save verification until user has actually been actiavted
            success_message = 'Verification was successfull. You can now proceed to sign in to your account.'
            return render(request, 'accounts/signin/index.html', {'success_message': success_message, 'form': form})
        except Exception as e:
            return HttpResponse('An error occurred while trying to verify your account. ' + str(e))
