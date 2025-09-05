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




import stripe
from django.conf import settings

from django.core.mail import send_mail
from django.urls import reverse

from .pricing import get_registration_price

stripe.api_key = settings.STRIPE_SECRET_KEY


from django.core.mail import EmailMessage
from .utils import generate_invoice_pdf


 

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from .models import Participant, REGISTRATION_CHOICES

 
 
 

# views.py
 
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from formtools.wizard.views import SessionWizardView

from .forms import UserForm, ParticipantForm, REGISTRATION_PRICES
 



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










def payment_success(request, pk):
    participant = Participant.objects.get(pk=pk)
    participant.paid = True
    participant.save()

    # Generate PDF
    pdf_buffer = generate_invoice_pdf(participant)

    # Render HTML email
    subject = "Registration Confirmation - AIML 2025"
    from_email = "info@aiml-paris.com"
    to = [participant.email]

    html_content = render_to_string("aiml_app/email_confirmation.html", {"participant": participant})
    text_content = f"Dear {participant.name},\n\nThank you for registering for AIML 2025 - Paris. Your payment has been confirmed.\n\nAmount Paid: ${participant.amount_paid}\nRegistration Type: {participant.get_registration_type_display()}\n\nA PDF invoice is attached.\n\nSee you at the event!"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.attach(f"Invoice_{participant.id}.pdf", pdf_buffer.read(), "application/pdf")
    msg.send()

    return render(request, "success.html", {"participant": participant})




def payment_cancel(request):
    return render(request, "cancel.html")



def send_reminder_email():
    event = Event.objects.get(slug="aiml-2025-paris")  # your event instance
    participants = Participant.objects.filter(paid=True)

    for participant in participants:
        subject = f"Reminder: AIML 2025 - Paris Conference"
        from_email = "info@aiml-paris.com"
        to = [participant.email]

        html_content = render_to_string("aiml_app/email_reminder.html", {
            "participant": participant,
            "event": event
        })

        text_content = f"Dear {participant.name},\n\nThis is a reminder that you are registered for AIML 2025 - Paris.\nEvent Dates: {event.start_date} - {event.end_date}\nLocation: {event.location}\n\nSee you there!"

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()







from django.shortcuts import render, redirect
from .forms import UserForm, ParticipantForm
from django.contrib.auth import login

def multi_step_registration(request):
    if request.method == 'POST':
        step = request.POST.get('step')
        if step == '1':
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                request.session['user_data'] = user_form.cleaned_data
                participant_form = ParticipantForm()
                return render(request, 'aiml_app/registration_step2.html', {'form': participant_form})
        elif step == '2':
            participant_form = ParticipantForm(request.POST)
            if participant_form.is_valid():
                # Create user
                user_data = request.session.get('user_data')
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    password=user_data['password']
                )
                participant = participant_form.save(commit=False)
                participant.user = user
                participant.save()
                login(request, user)
                return redirect('registration_success')
    else:
        user_form = UserForm()
    return render(request, 'aiml_app/registration_step1.html', {'form': user_form})


from formtools.wizard.views import SessionWizardView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserForm, ParticipantForm
from .models import Participant, REGISTRATION_PRICES
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

FORMS = [
    ("user", UserForm),
    ("participant", ParticipantForm),
]

TEMPLATES = {
    "user": "aiml_app/registration_wizard_user.html",
    "participant": "aiml_app/registration_wizard_participant.html",
}

class RegistrationWizard(SessionWizardView):
    form_list = [UserForm, ParticipantForm]
    template_name = "registration/wizard_form.html"

    def get_template_names(self):
        # Always use the same template for all steps
        return [self.template_name]

    def done(self, form_list, **kwargs):
        # Step 1: UserForm
        user_form = form_list[0]
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data["password"])
        user.save()

        # Step 2: ParticipantForm
        participant_form = form_list[1]
        participant = participant_form.save(commit=False)
        participant.user = user
        participant.registration_fee = REGISTRATION_PRICES.get(
            participant.registration_type, 0
        )
        participant.save()

        login(self.request, user)
        return redirect("registration_success")



def done(self, form_list, **kwargs):
    data = {}
    for form in form_list:
        data.update(form.cleaned_data)

    # Save data to your Participant/User models here

    return render(self.request, 'aiml_app/registration_done.html', context=data)





# Success Page
def registration_success(request):
    return render(request, "registration/success.html")

