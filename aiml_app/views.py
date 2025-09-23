# aiml_app/views.py
from datetime import datetime, timezone
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import ImportantDate, Speaker
from .forms import SpeakerForm
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


from .forms import UserForm

from django.views.decorators.http import require_GET

import stripe
from django.conf import settings

from django.core.mail import send_mail
from django.urls import reverse

from .pricing import get_registration_price

stripe.api_key = "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"





from django.core.mail import EmailMessage
from .utils import generate_invoice_pdf, is_late_registration


 

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



 
 
 

# views.py
 
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from formtools.wizard.views import SessionWizardView


 

 
def index(request):
    return render(request, 'aiml_app/index.html')


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



def registration_information(request):
    return render(request, 'aiml_app/registration_information.html')



# User Registration view pages :


def registration(request):
    return render('request', 'aiml_app/registration.html')


# Why attend ? :

def why_attend(request):
    return render(request, 'aiml_app/why_attend.html')



def Important_Date(request):
    infos = ImportantDate.objects.all()
    return render(request, 'aiml_aiml/registration_information.html', {'infos': infos} )


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


# aiml_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from formtools.wizard.views import SessionWizardView
from django.views.decorators.csrf import csrf_exempt
from .forms import ParticipantPersonalForm, ParticipantRegistrationForm
from .models import ParticipantRegistration
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

FORMS = [
    ("personal", ParticipantRegistration),
    ("registration", ParticipantRegistrationForm),
]

TEMPLATES = {
    "personal": "wizard/personal_form.html",
    "registration": "wizard/registration_form.html",
}

class ParticipantWizard(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Merge form data
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        participant = ParticipantRegistration(**data)
        participant.fee_paid = participant.calculate_fee()
        participant.save()

        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{participant.get_category_display()} registration"
                    },
                    "unit_amount": int(participant.fee_paid * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=self.request.build_absolute_uri(f"/aiml_app/success/{participant.id}/"),
            cancel_url=self.request.build_absolute_uri("/aiml_app/canceled/"),
        )

        participant.stripe_session_id = session.id
        participant.save()

        return redirect(session.url, code=303)
    


def check_email(request):
    email = request.GET.get('email', None)
    exists = ParticipantRegistration.objects.filter(email__iexact=email).exists() if email else False
    return JsonResponse({'exists': exists})


# Dynamic fee AJAX
@csrf_exempt
def get_fee(request):
    category = request.GET.get("category")
    reg_type = request.GET.get("reg_type")

    if not category or not reg_type:
        return JsonResponse({"fee": 0})

    dummy = ParticipantRegistration(category=category, reg_type=reg_type)
    fee = dummy.calculate_fee()
    return JsonResponse({"fee": fee})

def registration_success(request, pk):
    participant = ParticipantRegistration.objects.get(pk=pk)
    return render(request, "wizard/success.html", {"participant": participant})

def registration_canceled(request):
    return render(request, "wizard/canceled.html")


 
# Stripe webhook
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        try:
            participant = ParticipantRegistration.objects.get(stripe_session_id=session["id"])
            participant.payment_status = "paid"
            participant.save()
        except ParticipantRegistration.DoesNotExist:
            pass

    elif event["type"] in ["checkout.session.expired", "checkout.session.async_payment_failed"]:
        session = event["data"]["object"]
        try:
            participant = ParticipantRegistration.objects.get(stripe_session_id=session["id"])
            participant.payment_status = "failed"
            participant.save()
        except ParticipantRegistration.DoesNotExist:
            pass

    return HttpResponse(status=200)




@require_GET
def check_email(request):
    email = request.GET.get("email", None)
    exists = ParticipantRegistration.objects.filter(email=email).exists()
    return JsonResponse({"exists": exists})



stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_page(request):
    return render(request, "payment_form.html", {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_payment_intent(request):
    try:
        intent = stripe.PaymentIntent.create(
            amount=10000,  # in cents — this is $100.00
            currency='usd',
            payment_method_types=["card"],
        )
        return JsonResponse({"clientSecret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



def payment_success(request):
    return render(request, "payment_success.html")



 

# views.py
 
from .models import EarlyRegistration, LateRegistration

def registration_fees(request):
    early_data = EarlyRegistration.objects.all()
    late_data = LateRegistration.objects.all()
    return render(request, "aiml_aiml/registration_information.html", {
        "early_data": early_data,
        "late_data": late_data,
    })


