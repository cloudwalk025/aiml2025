
# aiml_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
 
 

class Speaker(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='speakers/', null=True, blank=True)
    topic = models.CharField(max_length=200)
    talk_title = models.CharField(max_length=200)
    talk_summary = models.TextField()
    social_media = models.URLField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.talk_title}"
    
    class Meta:
        ordering = ['-approved_at']


class CarouselImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='carousel/')
    caption = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    link_url = models.URLField(blank=True)

    def __str__(self):
        return self.title or f"Carousel Image {self.id}"

    class Meta:
        ordering = ['-uploaded_at']

#Upcoming Events Model

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    registration_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='upcoming')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_event_type_display()}"
    
    class Meta:
        ordering = ['-event_date']
        
    @property
    def status(self):
        if self.event_date > timezone.now():
            return 'upcoming'
        return 'past'
    


# Partnership and Sponsorship Section 


class Partner(models.Model):
    PARTNER_TYPES = [
        ('industry', 'Industrial Partner'),
        ('media', 'Media Partner'),
        ('community', 'Community Partner'),
    ]
    
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    website = models.URLField()
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"

class Sponsor(models.Model):
    SPONSOR_TYPES = [
        ('platinum', 'Platinum - $10,000'),
        ('gold', 'Gold - $5,000'),
        ('silver', 'Silver - $2,500'),
        ('bronze', 'Bronze - $1,000'),
    ]
    
    organization = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField()
    sponsor_type = models.CharField(max_length=20, choices=SPONSOR_TYPES)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def sponsorship_amount(self):
        amounts = {
            'platinum': 10000,
            'gold': 5000,
            'silver': 2500,
            'bronze': 1000
        }
        return amounts.get(self.sponsor_type, 0)
    
    def __str__(self):
        return f"{self.organization} ({self.get_sponsor_type_display()})"
    

# View Agenda


class EventAgenda(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Higher numbers appear first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ['-order', '-created_at']
        verbose_name = "Event Agenda"
        verbose_name_plural = "Event Agendas"

 

 # Contact Model :

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    is_responded = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Internal notes about the response")

    def __str__(self):
        return f"{self.subject} - {self.name}"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Contacts" 



# Team Member Model : 

class TeamMember(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='team_members/')
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.designation}"
    
    class Meta:
        ordering = ['-approved_at']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        


# Create model for About_us, venue and Date


class AboutEvent(models.Model):
    event_name = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

class Venue(models.Model):
    venue_name = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.venue_name

class EventDate(models.Model):
    date_name = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date_name
        


# User Registration :
