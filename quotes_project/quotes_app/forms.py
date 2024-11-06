from django.contrib.auth.models import User
from django.utils.encoding import force_str
from .models import Author, Quote
from django import forms
from django import forms


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

    def clean(self):
        cleaned_data = super().clean()
        
        cleaned_data['fullname'] = force_str(cleaned_data.get('fullname', ''))
        cleaned_data['born_date'] = force_str(cleaned_data.get('born_date', ''))
        cleaned_data['born_location'] = force_str(cleaned_data.get('born_location', ''))
        cleaned_data['description'] = force_str(cleaned_data.get('description', ''))
        
        return cleaned_data

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        return password

