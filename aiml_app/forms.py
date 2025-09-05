# aiml_app/forms.py
from django import forms
from .models import Speaker
from .models import Partner, Sponsor

from .models import TeamMember
from .models import Contact 


from django.utils import timezone
from .models import User


from .models import Participant, REGISTRATION_CHOICES

 
from .models import Participant, REGISTRATION_PRICES
import re
from datetime import datetime

class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = [
            'name', 'email', 'phone', 'bio', 'profile_pic',
            'topic', 'talk_title', 'talk_summary', 'social_media'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'talk_summary': forms.Textarea(attrs={'rows': 4}),
        }


# Forms for Partnership and Sponsorship

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'website', 'partner_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = [
            'organization', 'logo', 'website', 'sponsor_type',
            'contact_name', 'contact_email', 'contact_phone'
        ]
        widgets = {
            'sponsor_type': forms.RadioSelect(),
        }

# User profile Registration Form 



# Contac Form :

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Your Message'
        }


# Team Member Request form :

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            'full_name', 'designation', 'institution', 'profile_picture',
            'linkedin_url', 'twitter_url', 'email'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
            'twitter_url': forms.URLInput(attrs={'placeholder': 'https://twitter.com/username'}),
        }
        labels = {
            'full_name': 'Full Name',
            'profile_picture': 'Profile Photo',
            'linkedin_url': 'LinkedIn Profile',
            'twitter_url': 'Twitter Profile'
        }


from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Participant, REGISTRATION_PRICES, PAYMENT_CHOICES
import re

User = get_user_model()

# Step 1 - User account form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise ValidationError("Passwords do not match.")
        return cleaned_data


# Step 2 - Participant details (NO card fields here)
class ParticipantForm(forms.ModelForm):
    registration_fee = forms.DecimalField(
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Participant
        fields = [
            "phone_number", "designation",
            "institution_name", "address", "country",
            "registration_type", "payment_option"
        ]

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not re.match(r"^\+?\d{7,15}$", phone):
            raise forms.ValidationError("Enter a valid phone number with country code.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        reg_type = cleaned_data.get("registration_type")
        if reg_type in REGISTRATION_PRICES:
            cleaned_data["registration_fee"] = REGISTRATION_PRICES[reg_type]
        return cleaned_data
