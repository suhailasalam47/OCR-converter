from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'email', 'username', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')  

        if password != confirm_password:
            raise forms.ValidationError(
                "Password not matching!"
            )  

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = "Email"  


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'email', 'username']
            
