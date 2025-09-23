# aiml_app/admin.py
from datetime import timezone
from django.contrib import admin
from .models import Speaker
from .models import CarouselImage
from .models import Event
from django.contrib import admin
from .models import Partner, Sponsor

from .models import EventAgenda

from .models import Contact 

from .models import TeamMember

from .models import AboutEvent, Venue, EventDate, ImportantDate

from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile





class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'phone_number', 'institution', 'department','designation', 'address', 'country', 'is_active')
   
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()






admin.site.register(User, CustomUserAdmin)


admin.site.register(UserProfile)
@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'talk_title', 'status', 'is_featured', 'submitted_at')
    list_filter = ('status', 'is_featured')
    search_fields = ('name', 'email', 'talk_title')
    actions = ['approve_speakers', 'make_featured']
    
    def approve_speakers(self, request, queryset):
        updated = queryset.update(status='approved', approved_at=timezone.now())
        self.message_user(request, f"{updated} speakers approved.")
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} speakers marked as featured.")
    
    approve_speakers.short_description = "Approve selected speakers"
    make_featured.short_description = "Mark selected as featured"



@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'uploaded_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title', 'caption')
    readonly_fields = ('uploaded_at',)




@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'event_date', 'event_type', 'is_featured')
    list_filter = ('event_type', 'is_featured')
    search_fields = ('title', 'venue', 'description')
    list_editable = ('is_featured',)
    date_hierarchy = 'event_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Event Details', {
            'fields': ('venue', 'event_date', 'registration_url')
        }),
        ('Classification', {
            'fields': ('event_type', 'is_featured')
        }),
    )



# Partnership and Sponsorship
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'status', 'created_at')
    list_filter = ('partner_type', 'status')
    search_fields = ('name', 'description')
    list_editable = ('status',)
    actions = ['approve_partners', 'reject_partners']
    
    def approve_partners(self, request, queryset):
        queryset.update(status='approved')
    approve_partners.short_description = "Approve selected partners"
    
    def reject_partners(self, request, queryset):
        queryset.update(status='rejected')
    reject_partners.short_description = "Reject selected partners"

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('organization', 'sponsor_type', 'status', 'created_at')
    list_filter = ('sponsor_type', 'status')
    search_fields = ('organization', 'contact_name')
    list_editable = ('status',)
    actions = ['approve_sponsors', 'reject_sponsors']
    
    def approve_sponsors(self, request, queryset):
        queryset.update(status='approved')
    approve_sponsors.short_description = "Approve selected sponsors"
    
    def reject_sponsors(self, request, queryset):
        queryset.update(status='rejected')
    reject_sponsors.short_description = "Reject selected sponsors"






# view Agenda

@admin.register(EventAgenda)
class EventAgendaAdmin(admin.ModelAdmin):
    list_display = ('topic', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('topic', 'description')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('topic', 'description', 'order', 'is_active')
        }),
    )
 



# Contact Admin

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'is_responded')
    list_filter = ('is_responded', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_responded',)
    readonly_fields = ('submitted_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Response Status', {
            'fields': ('is_responded', 'notes'),
            'classes': ('collapse',)
        }),
    )



# Team Member Admin :

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'designation', 'institution', 'status', 'requested_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'designation', 'institution')
    list_editable = ('status',)
    actions = ['approve_members']
    
    def approve_members(self, request, queryset):
        updated = queryset.update(status='approved', approved_at=timezone.now())
        self.message_user(request, f"{updated} members approved.")
    approve_members.short_description = "Approve selected members" 
    

# Admin for about_us, Date and Venue :

@admin.register(AboutEvent)
class AboutEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'updated_at')
    fields = ('event_name', 'description')

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'updated_at')
    fields = ('venue_name', 'description')

@admin.register(EventDate)
class EventDateAdmin(admin.ModelAdmin):
    list_display = ('date_name', 'updated_at')
    fields = ('date_name', 'description')



@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ('final_paper_submission', 'early_registration_date', 'late_registration_date', 'conference_date', 'updated_at')
    fields = ('abstract_submission', 'paper_submission', 'acceptance_notification', 'final_paper_submission', 'early_registration_date', 'late_registration_date', 'conference_date')




# Early Registration Date : 

from .models import EarlyRegistration
@admin.register(EarlyRegistration)
class EarlyRegistration(admin.ModelAdmin):
    list_display=('student_early_registration','author_early_registration', 'listener_early_registration', 'updated_at')
    fields = ('student_early_registration','author_early_registration', 'listener_early_registration')



# Late Registration Date : 

from .models import LateRegistration
@admin.register(LateRegistration)
class LateRegistration(admin.ModelAdmin):
    list_display=('student_late_registration','author_late_registration', 'listener_late_registration', 'updated_at')
    fields = ('student_late_registration','author_late_registration', 'listener_late_registration')



# User Registration Admin :

 
# admin.py
 


from django.contrib import admin
from .models import ParticipantRegistration

@admin.register(ParticipantRegistration)
class ParticipantRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'designation', 'institution', 'address_1', 'city' , 'state', 'postal_code', 'country', 'category', 'reg_type', 'registration_period', 'payment_status', 'fee_paid', 'paper_id', 'paper_title', 'created_date']
    list_filter = ['category', 'reg_type', 'payment_status', 'registration_period', 'is_author']
    search_fields = ['full_name', 'email', 'paper_id', 'paper_title']
