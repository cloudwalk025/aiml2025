# context_processors.py
from .models import ImportantDate

def important_dates(request):
    return {
        'infos': ImportantDate.objects.all()
    }

