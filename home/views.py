from django.shortcuts import render, get_object_or_404, redirect
from .forms import TicketBookingForm
from .models import TicketBooking
from django.utils import timezone

# ------------------ BASIC PAGES ------------------

def index_view(request):
    return render(request, 'home/index.html')

def about_view(request):
    return render(request, 'home/about.html')


# ------------------ STATION LIST ------------------

STATIONS = [
    {"name": "Vytilla", "lat": 9.9787, "lng": 76.2979},
    {"name": "High Court", "lat": 9.9822, "lng": 76.2765},
    {"name": "Vypin", "lat": 10.004, "lng": 76.233},
    {"name": "Kakkanad", "lat": 10.0197, "lng": 76.3572},
    {"name": "South Chittoor", "lat": 10.0346, "lng": 76.2907},
    {"name": "Cheranalloor", "lat": 10.0270, "lng": 76.2920},
    {"name": "Eloor", "lat": 10.0525, "lng": 76.3102},
    {"name": "Fort Kochi", "lat": 9.9659, "lng": 76.2426}
]


# ------------------ FARES ------------------

FARES = {
    ("Vytilla", "High Court"): 40,
    ("High Court", "Fort Kochi"): 40,
}

def get_fare(source, dest):
    if (source, dest) in FARES:
        return FARES[(source, dest)]
    if (dest, source) in FARES:
        return FARES[(dest, source)]
    if source == dest:
        return 20
    return 40
 #------------------ TICKET BOOKING ------------------

def book_ticket(request):
    booking = None   # latest booking to show on the right

    if request.method == "POST":
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
    else:
        form = TicketBookingForm()

    return render(request, "home/book_ticket.html", {
        "form": form,
        "booking": booking,
    })


# ------------------ MY BOOKINGS (LIST) ------------------

def my_bookings(request):
    bookings = TicketBooking.objects.order_by("-created_at")
    return render(request, "home/my_bookings.html", {"bookings": bookings})


# ------------------ CANCEL BOOKING ------------------

def cancel_booking(request, booking_id):
    booking = get_object_or_404(TicketBooking, id=booking_id)

    if request.method == "POST" and booking.status != "CANCELLED":
        booking.status = "CANCELLED"
        booking.cancelled_at = timezone.now()
        booking.save()

    return redirect("home:my_bookings")


# ------------------ JOURNEY PAGE ------------------

def journey(request):
    stations = [s["name"] for s in STATIONS]
    fare = route = src = dst = None

    if request.method == "POST":
        src = request.POST.get("source")
        dst = request.POST.get("destination")
        fare = get_fare(src, dst)
        route = [src, dst]

    return render(request, "home/journey.html", {
        "stations": stations,
        "fare": fare,
        "route": route,
        "src": src,
        "dst": dst,
        "stations_json": STATIONS,
    })


# ------------------ TERMINAL DETAILS ------------------

from django.shortcuts import render

# -----------------------------
# TERMINAL INFORMATION DATABASE
# -----------------------------
TERMINAL_INFO = {
    "Vytilla": {
        "description": "Vytilla is one of Kochi’s biggest mobility hubs connecting water metro, buses, and metro rail.",
        "points": [
            "Hill Palace Museum",
            "Mangalavanam Bird Sanctuary",
            "Marine Drive Walkway",
            "Fort Kochi & Chinese Fishing Nets",
            "Aluva & Edappally accessibility"
        ],
        "image": "home/images/terminals/vytilla.jpg"
    },

    "High Court": {
        "description": "Located beside Kochi High Court, this terminal serves the city’s major legal and commercial zone.",
        "points": [
            "Mangalavanam Bird Sanctuary",
            "Marine Drive Boat Jetty",
            "Broadway Market",
            "Jew Town & Spice Market",
            "Fort Kochi heritage attractions"
        ],
        "image": "home/images/terminals/highcourt.jpg"
    },

    "Vypin": {
        "description": "Vypin is a major island known for beaches, fishing communities, and heritage monuments.",
        "points": [
            "Cherai Beach",
            "Puthuvype Lighthouse",
            "Pallipuram Fort",
            "Njarakkal Fish Farm",
            "Vypin Backwaters"
        ],
        "image": "home/images/terminals/vypin.jpg"
    },

    "Kakkanad": {
        "description": "Kakkanad is Kochi’s IT hub, home to Infopark, SmartCity and major residential areas.",
        "points": [
            "Infopark Phase 1 & 2",
            "SmartCity Kochi",
            "Kakkanad Civil Station",
            "Rajagiri Valley",
            "Kadambrayar Eco Tourism"
        ],
        "image": "home/images/terminals/kakkanad.jpg"
    },

    "South Chittoor": {
        "description": "Located near the backwaters, South Chittoor offers scenic water routes and local residential access.",
        "points": [
            "Chittoor Shiva Temple",
            "Vaduthala Backwaters",
            "Bolgatty Island (Nearby)",
            "International Marina (Nearby)"
        ],
        "image": "home/images/terminals/south chittor.jpg"
    },

    "Cheranalloor": {
        "description": "A peaceful suburban terminal surrounded by waterways, temples, and residential communities.",
        "points": [
            "Amrita Hospital (Nearby)",
            "Varapuzha Backwaters",
            "St. James Church",
            "Cheranalloor Shiva Temple"
        ],
        "image": "home/images/terminals/cherry.jpeg"
    },

    "Eloor": {
        "description": "Eloor is an industrial and residential region connected through river networks.",
        "points": [
            "Eloor Ferry",
            "Pathalam Regulator Bridge",
            "Kadungalloor Temple",
            "Industrial zone landmarks"
        ],
        "image": "home/images/terminals/eloor.webp"
    },

    "Fort Kochi": {
        "description": "Fort Kochi is the historic and cultural heart of Kochi, famous for colonial-era architecture.",
        "points": [
            "Fort Kochi Beach",
            "Chinese Fishing Nets",
            "Mattancherry Palace (Dutch Palace)",
            "Santa Cruz Basilica",
            "Jew Town & Synagogue"
        ],
        "image": "home/images/terminals/fortkochi.webp"
    },

    "Willingdon Island": {
        "description": "Willingdon Island is India’s largest artificial island, housing naval, port, and tourism centers.",
        "points": [
            "Cochin Port",
            "Southern Naval Command",
            "Taj Malabar Resort",
            "Ferry access to Fort Kochi",
            "Bolgatty Island (Nearby)"
        ],
        "image": "home/images/terminals/willingdon.jpg"
    },

    "Mattancherry": {
        "description": "Mattancherry is a heritage-rich locality famous for spice markets, palaces, and diverse communities.",
        "points": [
            "Jew Town",
            "Mattancherry Palace",
            "Paradesi Synagogue",
            "Antique Market Street",
            "Harbour Walkways"
        ],
        "image": "home/images/terminals/mattancherry.jpg"
    },
}

# --------------------------------------
# TERMINAL DETAIL VIEW FUNCTION
# --------------------------------------
def terminal_detail(request, name):
    info = TERMINAL_INFO.get(name)

    if not info:
        return render(request, "home/terminal_not_found.html")

    return render(request, "home/terminal_detail.html", {
        "name": name,
        "image": info["image"],

        "description": info["description"],
        "points": info.get("points", []),
    })
