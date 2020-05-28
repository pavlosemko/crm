from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class UserForm(forms.Form):
    full_name= forms.CharField()

