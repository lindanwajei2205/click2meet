from django.shortcuts import render, get_object_or_404
from .models import EventImage, Event
from bookings.models import Booking
from bookings.forms import BookingForm

def EventListView(request):
    events = Event.objects.all().prefetch_related('images').order_by('-created_at')
    context = {
        'events': events
    }
    return render(request, 'events/event_list.html', context)


def EventDetailView(request, event_id):
    event = get_object_or_404(
        Event.objects.all().prefetch_related('images', 'ticket_types'),
        pk=event_id
    )
    user_bookings = Booking.objects.filter(ticket_type__event=event, user=request.user)
    context = {
        'event': event,
        'images': event.images.all(),
        'ticket_types': event.ticket_types.all(),
        'form': BookingForm(),
        'user_bookings': user_bookings,
    }
    return render(request, 'events/event_detail.html', context)
