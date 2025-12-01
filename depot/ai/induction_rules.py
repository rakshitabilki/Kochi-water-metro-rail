from datetime import datetime, date

def compute_train_priority(train):
    now = datetime.now()
    today = date.today()

    priority = 0
    reasons = []

    # Fitness certificates
    if not train.certs.filter(valid_to__gte=now).exists():
        priority -= 100
        reasons.append("Fitness expired")
    else:
        reasons.append("Fitness valid")

    # Job card maintenance urgency
    jobcard = train.jobcards.order_by('-created_at').first()
    if jobcard and jobcard.next_maintenance_date:
        if jobcard.next_maintenance_date < today:
            priority += 30
            reasons.append("Maintenance overdue")

    # Mileage
    mileage = train.mileages.order_by('-recorded_at').first()
    if mileage and mileage.cumulative_mileage > 8000:
        priority += 20
        reasons.append("High mileage")

    # Branding exposure
    if train.branding:
        b = train.branding
        if b.achieved_hours < b.required_exposure_hours:
            priority += 10
            reasons.append("Branding hours pending")

    return priority, reasons
