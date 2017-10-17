from django import forms

__all__=(
    'SignupForm',
)

class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

