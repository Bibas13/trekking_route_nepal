from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking
import datetime


class BookingForm(forms.ModelForm):
    trek_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().isoformat()}),
        label='Trek Start Date'
    )
    trek_end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().isoformat()}),
        label='Trek End Date'
    )

    class Meta:
        model = Booking
        fields = [
            'full_name', 'email', 'phone', 'nationality',
            'trek_start_date', 'trek_end_date', 'num_trekkers',
            'require_guide', 'require_porter', 'num_porters',
            'emergency_contact_name', 'emergency_contact_phone',
            'special_requests'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+977 9800000000'}),
            'nationality': forms.TextInput(attrs={'placeholder': 'e.g. American, British, Indian'}),
            'num_trekkers': forms.NumberInput(attrs={'min': 1, 'max': 50}),
            'num_porters': forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'emergency_contact_name': forms.TextInput(attrs={'placeholder': 'Emergency contact full name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'placeholder': '+1 555 000 0000'}),
            'special_requests': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any dietary restrictions, medical conditions, or special needs...'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('trek_start_date')
        end = cleaned_data.get('trek_end_date')
        if start and end and end <= start:
            raise forms.ValidationError('End date must be after start date.')
        return cleaned_data


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
