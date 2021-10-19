from django import forms 


class LoginForm(forms.Form):
    name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'username'}))
    # email = forms.EmailField(max_length=200, label='', widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'email'}))
    password = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'password'}))

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'username'}))
    #email = forms.EmailField(max_length=200, label='', widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'email'}))
    password = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={'type': 'password', 'placeholder': 'password'}))

    



    