from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from verification.models import PhoneVerification
from django.http import HttpResponseRedirect, HttpResponse


@login_required(login_url='/accounts/signin/')
def index(request):
    # check if there are any pending phone verifications
    user = request.user
    try:
        phone_verification = PhoneVerification.objects.get(
            user=user, active=1, verified=0)
        phone_verification.active = 0
        phone_verification.verified = 1
        phone_verification.save()
        # redirect the user back to verification
        return HttpResponseRedirect('/verification/')
    except PhoneVerification.DoesNotExist:
        return render(request, 'dashboard/index.html', {'user': user})
