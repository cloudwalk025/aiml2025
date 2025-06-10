# aiml_app/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RegistrationFlowMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip middleware for these views
        exempt_views = [
            'registration_home',
            'registration_personal',
            'registration_confirmation',
            'participant_list',
            'participant_edit',
            'participant_delete'
        ]
        
        if view_func.__name__ in exempt_views:
            return None
        
        # Check if user has completed previous steps
        if 'participant_data' not in request.session:
            return redirect('registration_personal')
        
        current_view = view_func.__name__
        
        if current_view == 'registration_organizational' and 'personal' not in request.session['participant_data']:
            return redirect('registration_personal')
            
        if current_view == 'registration_preferences' and 'organizational' not in request.session['participant_data']:
            return redirect('registration_organizational')
            
        if current_view == 'registration_payment' and 'preferences' not in request.session['participant_data']:
            return redirect('registration_preferences')
        
        return None