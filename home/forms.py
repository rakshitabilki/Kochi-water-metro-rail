from django import forms
from .models import TicketBooking

class TicketBookingForm(forms.ModelForm):
    journey_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = TicketBooking
        fields = [
            "source",
            "destination",
            "journey_date",
            "passenger_name",
            "passenger_phone",
            "no_of_tickets",
        ]
