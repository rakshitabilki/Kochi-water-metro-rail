from django.db import models

# Create your models here.
class TicketBooking(models.Model):
    SOURCE_CHOICES = [
        ("Vytilla", "Vytilla"),
        ("High Court", "High Court"),
        ("Vypin", "Vypin"),
        ("Kakkanad", "Kakkanad"),
        ("South Chittoor", "South Chittoor"),
        ("Cheranalloor", "Cheranalloor"),
        ("Eloor", "Eloor"),
        ("Fort Kochi", "Fort Kochi"),
        ("Willingdon Island", "Willingdon Island"),
        ("Mattancherry", "Mattancherry"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CANCELLED", "Cancelled"),
    ]

    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    destination = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    journey_date = models.DateField()
    passenger_name = models.CharField(max_length=100)
    passenger_phone = models.CharField(max_length=20)
    no_of_tickets = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # for cancelling
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="ACTIVE"
    )
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.passenger_name} - {self.source} to {self.destination} on {self.journey_date}"

# Create your models here.
