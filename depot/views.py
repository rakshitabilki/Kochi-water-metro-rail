# -----------------------------------------------------------
# VOLUNTEER DASHBOARD + ALL 6 FEATURE DETAIL PAGES + API
# -----------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Trainset
from .forms import  JobCardDetailForm

from .models import Trainset, FitnessCertificate, JobCard, Branding, CleaningSlot, Bay,Mileage
from .forms import (
    AddTrainForm, FitnessDetailForm, JobCardDetailForm,
    BrandingDetailForm, MileageDetailForm, CleaningDetailForm,
    GeometryDetailForm,InductionDecision
)
from depot.ai.or_scheduler import schedule_induction   # <-- Add import


# -----------------------------------------------------------
# MAIN DASHBOARD
# -----------------------------------------------------------
@login_required
def dashboard(request):
    trains = Trainset.objects.select_related('branding', 'stabling_bay').all()
    latest = InductionDecision.objects.order_by('-created_at').first()
    decisions = {}
    if latest and latest.ranked_list:
        for item in latest.ranked_list:
            decisions[item['train']] = item

    return render(request, 'depot/dashboard.html', {
        'trains': trains,
        'decisions': decisions,
        'decision_run_date': latest.run_date if latest else None,
    })
# -----------------------------------------------------------
# JOB CARD STATUS DASHBOARD
# -----------------------------------------------------------

@login_required
def fitness(request):
    now = timezone.now()
    items = []
    for t in Trainset.objects.all():
        cert = t.certs.order_by('-valid_to').first()
        items.append({
            'train': t,
            'cert': cert,
            'is_valid': cert.is_valid(now) if cert else False
        })
    return render(request, 'depot/fitness.html', {'items': items})


@login_required
def job_card_status(request):
    items = []
    for t in Trainset.objects.all():
        jc = t.jobcards.order_by('-created_at').first()
        items.append({
            'train': t,
            'jobcard': jc,
        })
    return render(request, 'depot/job_card_status.html', {'items': items})


@login_required
def branding(request):
    return render(request, "depot/branding.html")



@login_required
def mileage(request):
    trains = Trainset.objects.all()
    return render(request, 'depot/mileage.html', {'trains': trains})


@login_required
def cleaning(request):
    slots = CleaningSlot.objects.select_related('assigned_trainset', 'bay')
    return render(request, 'depot/cleaning.html', {'slots': slots})


@login_required
def geometry(request):
    trains = Trainset.objects.select_related('stabling_bay')
    return render(request, 'depot/geometry.html', {'trains': trains})
# -----------------------------------------------------------
# FITNESS API for JS Dashboard
# -----------------------------------------------------------
@login_required
def api_fitness_data(request):
    now = timezone.now()

    # Preload certificates to avoid N+1 query problem
    trains = Trainset.objects.prefetch_related('certs')

    data = []

    for t in trains:
        cert = t.certs.order_by('-valid_to').first()   # latest certificate

        if cert:
            data.append({
                "train_number": t.number,
                "train_name": t.train_name or t.number,

                "department": cert.department,
                "valid_from": cert.valid_from.strftime("%Y-%m-%d %H:%M"),
                "valid_to": cert.valid_to.strftime("%Y-%m-%d %H:%M"),
                "doc": cert.doc,

                "isValid": cert.is_valid(now),
            })
        else:
            # If no certificate exists
            data.append({
                "train_number": t.number,
                "train_name": t.train_name or t.number,

                "department": "N/A",
                "valid_from": "-",
                "valid_to": "-",
                "doc": "",

                "isValid": False,
            })

    return JsonResponse({"fitness": data})



@login_required
def api_branding_data(request):
    data = []

    for t in Trainset.objects.select_related('branding'):
        data.append({
            "train_number": t.number,
            "train_name": t.train_name or "",
            "brand": t.branding.name if t.branding else "None",
            "required": t.branding.required_exposure_hours if t.branding else 0,
            "achieved": t.branding.achieved_hours if t.branding else 0,
        })

    return JsonResponse({"branding": data})


@login_required
def api_jobcard_data(request):
    data = []

    for t in Trainset.objects.all():
        job = t.jobcards.order_by('-created_at').first()   # latest job card

        if job:
            data.append({
                "train_number": t.number,
                "train_name": t.train_name,   # optional, you added this field

                "jobcard_id": job.jobcard_id,
                "assigned_task": job.assigned_task,
                "status": job.status,

                "last_service_date": job.last_service_date.strftime("%Y-%m-%d") if job.last_service_date else None,
                "next_maintenance_date": job.next_maintenance_date.strftime("%Y-%m-%d") if job.next_maintenance_date else None,

                "operator": job.operator,
                "remarks": job.remarks,

                "created_at": job.created_at.strftime("%Y-%m-%d %H:%M"),
            })

        else:
            # No job card exists → return placeholder
            data.append({
                "train_number": t.number,
                "train_name": t.train_name,

                "jobcard_id": None,
                "assigned_task": None,
                "status": "No Records",

                "last_service_date": None,
                "next_maintenance_date": None,

                "operator": None,
                "remarks": None,

                "created_at": None,
            })

    return JsonResponse({"jobcards": data})

@login_required
def api_mileage_data(request):
    data = []

    for t in Trainset.objects.all():
        data.append({
            "train_number": t.number,
            "train_name": t.train_name,
            "last_mileage": t.last_mileage,
            "cumulative_mileage": t.cumulative_mileage,
        })

    return JsonResponse({"mileage": data})




@login_required
def api_cleaning_data(request):
    data = []

    # Fetch all cleaning slots with related bay and trainset
    slots = CleaningSlot.objects.select_related("bay", "assigned_trainset").all()

    for s in slots:
        data.append({
            "train_number": s.assigned_trainset.number if s.assigned_trainset else None,
            "train_name": s.assigned_trainset.train_name if s.assigned_trainset else None,
            "bay_name": s.bay.name,
            "bay_position": s.bay.position,
            "start_time": s.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": s.end_time.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({"cleaning": data})


@login_required
def api_geometry_data(request):
    data = []

    for t in Trainset.objects.select_related("stabling_bay"):
        bay = t.stabling_bay

        data.append({
            "train_number": t.number,
            "train_name": t.train_name,
            "bay_name": bay.name if bay else "None",
            "bay_position": bay.position if bay else None,
            "bay_capacity": bay.capacity if bay else None,
        })

    return JsonResponse({"geometry": data})


# ---------- FITNESS DETAIL ----------
@login_required
def fitness_detail(request, number):
    train = get_object_or_404(Trainset, number=number)
    cert = train.certs.order_by('-valid_to').first()

    if request.method == "POST":
        form = FitnessDetailForm(request.POST, instance=cert)
        if form.is_valid():
            new_cert = form.save(commit=False)
            new_cert.trainset = train
            new_cert.save()
            messages.success(request, "Fitness saved.")
            return redirect('depot:jobcard_detail', number=number)
    else:
        form = FitnessDetailForm(instance=cert)

    return render(request, 'depot/details/fitness_detail.html', {
        'train': train, 'cert': cert, 'form': form
    })


# ---------- JOBCARD DETAIL ----------
@login_required
def jobcard_detail(request, number):
    train = get_object_or_404(Trainset, number=number)
    job = train.jobcards.order_by('-created_at').first()
    if not job:
        job = JobCard(trainset=train, jobcard_id='UNKNOWN', assigned_task='', status='Pending', operator='', remarks='')
        job.save()

    if request.method == "POST":
        form = JobCardDetailForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job card saved.")
            return redirect('depot:branding_detail', number=number)
    else:
        form = JobCardDetailForm(instance=job)

    return render(request, 'depot/details/jobcard_detail.html', {
        'train': train, 'form': form, 'job': job
    })


# ---------- BRANDING DETAIL ----------
@login_required
def branding_detail(request, number):
    train = get_object_or_404(Trainset, number=number)
    brand = train.branding

    if request.method == "POST":
        form = BrandingDetailForm(request.POST, instance=brand)
        if form.is_valid():
            b = form.save()
            train.branding = b
            train.save()
            messages.success(request, "Branding saved.")
            return redirect('depot:mileage_detail', number=number)
    else:
        form = BrandingDetailForm(instance=brand)

    return render(request, 'depot/details/branding_detail.html', {
        'train': train, 'form': form
    })


# ---------- MILEAGE DETAIL ----------
@login_required
def mileage_detail(request, number):
    train = get_object_or_404(Trainset, number=number)
    if request.method == "POST":
        form = MileageDetailForm(request.POST, instance=train)
        if form.is_valid():
            form.save()
            messages.success(request, "Mileage updated.")
            return redirect('depot:cleaning_detail', number=number)
    else:
        form = MileageDetailForm(instance=train)

    return render(request, 'depot/details/mileage_detail.html', {
        'train': train, 'form': form
    })

# ---------- CLEANING DETAIL ----------
@login_required
def cleaning_detail(request, number):
    train = get_object_or_404(Trainset, number=number)
    slots = CleaningSlot.objects.filter(assigned_trainset=train).order_by('start_time')
    if request.method == "POST":
        form = CleaningDetailForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            if not slot.assigned_trainset:
                slot.assigned_trainset = train
            slot.save()
            messages.success(request, "Cleaning slot created.")
            return redirect('depot:geometry_detail', number=number)
    else:
        form = CleaningDetailForm(initial={'assigned_trainset': train})

    return render(request, 'depot/details/cleaning_detail.html', {
        'train': train, 'form': form, 'slots': slots
    })
@login_required
def geometry_detail(request, number):
    train = get_object_or_404(Trainset, number=number)
    if request.method == "POST":
        form = GeometryDetailForm(request.POST)
        if form.is_valid():
            new_bay = form.cleaned_data.get('stabling_bay')
            train.stabling_bay = new_bay
            train.save()
            messages.success(request, "Stabling updated.")
            return redirect('depot:dashboard')
    else:
        form = GeometryDetailForm(initial={'stabling_bay': train.stabling_bay})

    return render(request, 'depot/details/geometry_detail.html', {
        'train': train, 'form': form, 'bay': train.stabling_bay
    })
# -----------------------------------------------------------
# AI INDUCTION SCHEDULING API
# -----------------------------------------------------------

@login_required
def api_induction_schedule(request):
    """
    Runs AI induction planning using rule-based priority + OR-Tools.
    Returns JSON schedule and saves decision to DB.
    """
    plan = schedule_induction()

    if plan is None:
        return JsonResponse({"error": "No feasible schedule found"}, status=400)

    # Save the AI decision
    from .models import InductionDecision
    decision = InductionDecision.objects.create(
        run_date=timezone.now().date(),
        ranked_list=plan,
        notes="Generated by AI Scheduler"
    )

    return JsonResponse({
        "generated_at": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        "decision_id": decision.id,
        "count": len(plan),
        "schedule": plan
    })
@login_required
def induction_schedule_view(request):
    """
    Show AI induction schedule in HTML format (table view).
    """
    from depot.ai.or_scheduler import schedule_induction
    
    plan = schedule_induction()     # Run AI
    return render(request, "depot/scheduler_latest.html", {
        "plan": plan
    })
# ADD TRAIN PAGE
# -----------------------------------------------------------
@login_required
def add_train(request):
    """
    Add a new train or edit basic fields (number, train_name, cars, notes).
    After saving, redirect to fitness_detail page.
    """
    if request.method == "POST":
        form = AddTrainForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number'].strip()

            # If train already exists → update existing
            existing_train = Trainset.objects.filter(number=number).first()
            if existing_train:
                existing_train.train_name = form.cleaned_data['train_name']
                existing_train.cars = form.cleaned_data['cars']
                existing_train.notes = form.cleaned_data['notes']
                existing_train.save()

                messages.info(request, f"Train {number} already exists — updated details.")
                return redirect('depot:fitness_detail', number=number)

            # Create NEW TRAIN
            new_train = form.save()
            messages.success(request, f"Train {new_train.number} created successfully!")

            return redirect('depot:fitness_detail', number=new_train.number)

    else:
        form = AddTrainForm()

    return render(request, 'depot/add_train.html', {'form': form})

   

