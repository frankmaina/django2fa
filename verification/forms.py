from django import forms


class VerificationCodeForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Enter the verification code")
