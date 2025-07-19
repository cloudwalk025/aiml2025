# aiml_app/views.py
from datetime import datetime, timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Speaker
from .forms import SpeakerForm, UserForm
from django.contrib import messages
from .models import Event, Speaker, CarouselImage
from .forms import PartnerForm, SponsorForm
from .models import Partner, Sponsor
 
from .models import EventAgenda

from .forms import ContactForm
from .models import Contact

from .models import TeamMember
from .forms import TeamMemberForm
from .models import AboutEvent, Venue, EventDate
from .models import User



# aiml_app/views.py


def agenda_view(request):
    agenda_items = EventAgenda.objects.filter(is_active=True)
    return render(request, 'aiml_app/agenda.html', {'agenda_items': agenda_items})



def index(request):
     # Featured speakers
    featured_speakers = Speaker.objects.filter(
        is_featured=True,
        status='approved'
    ).order_by('-approved_at')[:8]  # Get 4 most recently approved featured speakers
   
   
    # Carousel images  
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('-uploaded_at')[:5]
  

    # Get the most recent entries for each section
    about_event = AboutEvent.objects.last()
    venue = Venue.objects.last()
    event_date = EventDate.objects.last()


      # New event queries
    now = datetime.now(timezone.utc)
    upcoming_events = Event.objects.filter(
        event_date__gte=now,
        event_type='upcoming'
    ).order_by('event_date')[:3]
    
    past_events = Event.objects.filter(
        event_date__lt=now,
        event_type='past'
    ).order_by('-event_date')[:3]


    featured_partners = Partner.objects.filter(status='approved').order_by('-created_at')
    featured_sponsors = Sponsor.objects.filter(status='approved').order_by('sponsor_type')
    
    # Group sponsors by type
    platinum_sponsors = featured_sponsors.filter(sponsor_type='platinum')
    gold_sponsors = featured_sponsors.filter(sponsor_type='gold')
    silver_sponsors = featured_sponsors.filter(sponsor_type='silver')
    bronze_sponsors = featured_sponsors.filter(sponsor_type='bronze')

    agenda_items = EventAgenda.objects.filter(is_active=True)[:5] 

    context = {
        'featured_speakers': featured_speakers,
        'speakers_count': featured_speakers.count(),
        'carousel_images': carousel_images,
        'has_carousel_images': carousel_images.exists(),
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'has_upcoming_events': upcoming_events.exists(),
        'has_past_events': past_events.exists(),

        'featured_partners': featured_partners,
        'platinum_sponsors': platinum_sponsors,
        'gold_sponsors': gold_sponsors,
        'silver_sponsors': silver_sponsors,
        'bronze_sponsors': bronze_sponsors,

        'agenda_items': agenda_items,
        'has_agenda_items': agenda_items.exists(),

        'about_event': about_event,
        'venue': venue,
        'event_date': event_date,
    }
    return render(request, 'aiml_app/index.html', context)

def upcoming_events(request):
    now = datetime.now(timezone.utc)
    events = Event.objects.filter(
        event_date__gte=now,
        event_type='upcoming'
    ).order_by('event_date')
    
    return render(request, 'aiml_app/upcoming_events.html', {
        'events': events,
        'has_events': events.exists()
    })

def speaker_request(request):
    if request.method == 'POST':
        form = SpeakerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('speaker_thanks')
    else:
        form = SpeakerForm()
    return render(request, 'aiml_app/speaker_request.html', {'form': form})

def speaker_thanks(request):
    return render(request, 'aiml_app/speaker_thanks.html')

class FeaturedSpeakersView(ListView):
    model = Speaker
    template_name = 'aiml_app/featured_speakers.html'
    context_object_name = 'speakers'
    
    def get_queryset(self):
        return Speaker.objects.filter(is_featured=True, status='approved')
    


# Partnership and Sponsorship

def partner_request(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('partner_thanks')
    else:
        form = PartnerForm()
    return render(request, 'aiml_app/partner_request.html', {'form': form})

def sponsor_request(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sponsor_thanks')
    else:
        form = SponsorForm()
    return render(request, 'aiml_app/sponsor_request.html', {'form': form})

def partner_thanks(request):
    return render(request, 'aiml_app/partner_thanks.html')

def sponsor_thanks(request):
    return render(request, 'aiml_app/sponsor_thanks.html')



# User Registration view pages :


def registration(request):
    return render('request', 'aiml_app/registration.html')


# Why attend ? :

def why_attend(request):
    return render('request', 'aiml_app/why_attend.html')




# Contact Form :

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    # Get contact information to display (you can add this to your admin later)
    contact_info = {
        'email': 'info@cloudwalksoftware.com',
        'phone': '+1 (250) 207-9141',
        'address': '2270 Clifee Ave, Courtenay, BC V9N 2L4, Canada'
    }
    
    return render(request, 'aiml_app/contact.html', {
        'form': form,
        'contact_info': contact_info
    })



# Team member views : 

def team_member_request(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your team membership request has been submitted! We will review it soon.')
            return redirect('team_member_request')
    else:
        form = TeamMemberForm()
    
    return render(request, 'aiml_app/team_member_request.html', {'form': form})

def team_members_list(request):
    members = TeamMember.objects.filter(status='approved').order_by('-approved_at')
    return render(request, 'aiml_app/team_members.html', {'team_members': members})



# Registration Views : 

def registerUser(request):
    if request.method == 'POST':
      
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the User using the form 
          #  password = form.cleaned_data['password']
           # user = form.save(commit=False)
          #  user.set_password(password)
          #  user.role = User.PARTICIPANT
          #  user.save()

# Create the user using create user method 

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.PARTICIPANT
            user.save()
          
            return redirect('registerUser')
        
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = UserForm()
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'aiml_app/registerUser.html', context)