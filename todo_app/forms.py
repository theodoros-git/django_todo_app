from django import forms
from django.core.validators import validate_email
from .models import *
from django.core.exceptions import ValidationError




class JoinForm(forms.Form):

    email = forms.EmailField(

    	error_messages={'required': "This field is required."},
        validators=[validate_email],
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "enter your e-mail",                
                "class": "form-control",
            }
        ))


    password = forms.CharField(
    	error_messages={'required': "This field is required."},
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Create a password",                
                "class": "form-control",
            }
        ))    

    confirm_password = forms.CharField(

    	error_messages={'required': "This field is required."},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':"confirm your password",
                "class": "form-control",
            }
        )
    )


    def clean(self):
        cleaned_data = super().clean()
        mdp1 = cleaned_data.get("password")
        mdp2 = cleaned_data.get("confirm_password")

        if mdp1 and mdp2 and mdp1 != mdp2:
            raise ValidationError(
                "Passwords should be the same!"
                
            )



class LoginForm(forms.Form):

    email = forms.EmailField(

    	error_messages={'required': "This field is required."},
        validators=[validate_email],
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "enter your e-mail",                
                "class": "form-control",
            }
        ))


    password = forms.CharField(
    	error_messages={'required': "This field is required."},
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Create a password",                
                "class": "form-control",
            }
        ))


class TaskForm(forms.Form):

    name = forms.CharField(
        error_messages={'required': 'This field is required'},
        widget=forms.TextInput(
            attrs={
                "class": "form-control "
            }
        )
    )    

    
