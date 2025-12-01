# depot/rules.py
from django.utils import timezone
from .models import FitnessCertificate, JobCard, Branding

REQUIRED_DEPARTMENTS = {'Rolling-Stock', 'Signalling', 'Telecom'}

def check_fitness(trainset, at_time=None):
    """
    Returns (ok: bool, reason: str)
    """
    at_time = at_time or timezone.now()
    certs = trainset.certs.filter(valid_from__lte=at_time, valid_to__gte=at_time)
    depts = {c.department for c in certs}
    missing = REQUIRED_DEPARTMENTS - depts
    if missing:
        return False, "Missing certificates: " + ", ".join(sorted(missing))
    return True, ""

def check_jobcards(trainset):
    """
    Return (ok, reason) - True if no blocking open jobcards
    Simple policy: any open jobcard blocks induction. Adjust if required.
    """
    open_j = trainset.jobcards.filter(status__iexact='open').exists()
    if open_j:
        return False, "Open jobcards exist"
    return True, ""

def check_cleaning_assigned(trainset, at_time=None):
    """
    Very basic: check if trainset has a cleaning slot assigned that ends before next morning (example).
    Adjust policy as needed.
    """
    at_time = at_time or timezone.now()
    assigned = trainset.cleaningslot_set.filter(assigned_trainset=trainset).exists()
    if not assigned:
        return False, "No cleaning slot assigned"
    return True, ""

def branding_priority(trainset):
    """
    Higher value => higher priority to push into service.
    Compute shortfall = required - achieved. If no branding, return 0.
    """
    br = getattr(trainset, 'branding', None)
    if not br:
        return 0
    try:
        shortfall = (br.required_exposure_hours or 0) - (br.achieved_hours or 0)
        return max(0, shortfall)
    except Exception:
        return 0

def is_eligible(trainset, at_time=None):
    """
    Run all checks and produce overall eligibility and reasons list.
    """
    checks = []
    ok_f, r_f = check_fitness(trainset, at_time)
    checks.append(('fitness', ok_f, r_f))
    ok_j, r_j = check_jobcards(trainset)
    checks.append(('jobcards', ok_j, r_j))
    ok_c, r_c = check_cleaning_assigned(trainset, at_time)
    checks.append(('cleaning', ok_c, r_c))
    eligible = all(c[1] for c in checks)
    reasons = [f"{c[0]}: {c[2]}" for c in checks if not c[1] and c[2]]
    return eligible, reasons
