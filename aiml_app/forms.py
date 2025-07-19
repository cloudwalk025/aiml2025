# aiml_app/forms.py
from django import forms
from .models import Speaker
from .models import Partner, Sponsor

from .models import TeamMember
from .models import Contact 


from django.utils import timezone
from .models import User



 
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




# User Registration Form : 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'phone_number', 'institution', 'department', 'designation', 'address', 'country','role']
