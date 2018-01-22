from django import forms

class login_form (forms.Form):
    user_id = forms.EmailField()
    user_password = forms.PasswordInput()