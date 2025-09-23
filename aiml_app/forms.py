# aiml_app/forms.py
from django import forms
from .models import ParticipantRegistration, Speaker
from .models import Partner, Sponsor

from .models import TeamMember
from .models import Contact 


from django.utils import timezone
from .models import User


 

 

import re
from datetime import datetime

from django import forms
from .models import Speaker

class SpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = [
            'name', 'email', 'phone', 'bio', 'profile_pic',
            'topic', 'talk_title', 'talk_summary', 'social_media'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'talk_title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'talk_summary': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'social_media': forms.URLInput(attrs={'class': 'form-control'}),
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



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'



# aiml_app/forms.py
from django import forms
from .models import ParticipantRegistration
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
import re


# Step 1
class ParticipantPersonalForm(forms.ModelForm):
    class Meta:
        model = ParticipantRegistration
        fields = ['full_name', 'email', 'phone', 'designation',  'institution', 'department',
                  'address_1', 'address_2', 'city', 'state', 'postal_code', 'country']
        widgets = {
            "country": CountrySelectWidget(),  # nice dropdown
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'address_2':
                field.required = False  # ✅ Only address_2 is optional
            else:
                field.required = True



        self.fields['phone'].widget.attrs.update({
            'pattern': r'^\+?\d{10,15}$',
            'title': 'Enter 10–15 digit phone number. Digits only. Optional + at start.',
            'inputmode': 'numeric',
        })
        
# Step 2
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ParticipantRegistration.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Accept only digits, optionally allow country code format
        if not re.fullmatch(r'^\+?\d{10,15}$', phone):
            raise forms.ValidationError("Enter a valid phone number (10–15 digits, digits only).")
        return phone

class ParticipantRegistrationForm(forms.ModelForm):
    paper_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter Paper ID"})
    )
    paper_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter Paper Title"})
    )

    class Meta:
        model = ParticipantRegistration
        fields = ['category', 'reg_type', 'is_author', 'paper_id', 'paper_title']
        widgets = {
            'category': forms.Select(attrs={'id': 'id_category'}),
            'reg_type': forms.Select(attrs={'id': 'id_reg_type'}),
            'is_author': forms.CheckboxInput(attrs={'id': 'id_is_author'}),
            'paper_id': forms.TextInput(attrs={'id': 'id_paper_id'}),
            'paper_title': forms.TextInput(attrs={'id': 'id_paper_title'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_author = cleaned_data.get("is_author")
        if is_author:
            if not cleaned_data.get("paper_id"):
                self.add_error("paper_id", "Paper ID is required for authors.")
            if not cleaned_data.get("paper_title"):
                self.add_error("paper_title", "Paper Title is required for authors.")
        return cleaned_data



# Create a User Registration Form
 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
