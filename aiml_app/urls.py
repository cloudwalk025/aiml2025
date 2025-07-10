# aiml_app/urls.py
from django.urls import path
from .views import index, registration, speaker_request, speaker_thanks, FeaturedSpeakersView, upcoming_events
from .views import partner_request, sponsor_request, partner_thanks, sponsor_thanks
from .views import agenda_view, why_attend

from .views import contact_view 

from .views import team_member_request, team_members_list
from . import views



urlpatterns = [
    path('', index, name='index'),  # Homepage with featured speakers
    path('speaker/request/', speaker_request, name='speaker_request'),
    path('speaker/thanks/', speaker_thanks, name='speaker_thanks'),
    path('speakers/', FeaturedSpeakersView.as_view(), name='featured_speakers'),
    path('upcoming-events/', upcoming_events, name='upcoming_events'),
    path('partners/request/', partner_request, name='partner_request'),
    path('sponsors/request/', sponsor_request, name='sponsor_request'),
    path('partners/thanks/', partner_thanks, name='partner_thanks'),
    path('sponsors/thanks/', sponsor_thanks, name='sponsor_thanks'),
    path('registration/', registration, name='registration'),
    path('agenda/', agenda_view, name='agenda'),
    path('why_attend/', why_attend, name='why_attend'),
    path('contact/', contact_view, name='contact'),
    path('team/join/', team_member_request, name='team_member_request'),
    path('team/', team_members_list, name='team_members'),
    path('registerUser/', views.registerUser, name='registerUser')

    
]