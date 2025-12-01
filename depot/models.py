from django.db import models

class Trainset(models.Model):
    number = models.CharField(max_length=16, unique=True)   # e.g., "TS-01"
    train_name = models.CharField(max_length=64, blank=True)  # NEW FIELD

    cars = models.IntegerField(default=4)
    last_mileage = models.IntegerField(default=0)
    cumulative_mileage = models.IntegerField(default=0)

    branding = models.ForeignKey('Branding', null=True, blank=True, on_delete=models.SET_NULL)
    stabling_bay = models.ForeignKey('Bay', null=True, blank=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=32, default='idle')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.number} - {self.train_name}"

class FitnessCertificate(models.Model):
    trainset = models.ForeignKey(Trainset, on_delete=models.CASCADE, related_name='certs')
    department = models.CharField(max_length=64)   # Rolling-Stock / Signalling / Telecom
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    doc = models.CharField(max_length=255, blank=True)

    def is_valid(self, at_time):
        return self.valid_from <= at_time <= self.valid_to

class JobCard(models.Model):
    trainset = models.ForeignKey(Trainset, on_delete=models.CASCADE, related_name='jobcards')

    jobcard_id = models.CharField(max_length=50)         # New
    assigned_task = models.CharField(max_length=255)      # New
    status = models.CharField(max_length=50)              # New

    last_service_date = models.DateField(null=True, blank=True)  # New
    next_maintenance_date = models.DateField(null=True, blank=True)  # New

    operator = models.CharField(max_length=100)           # New
    remarks = models.TextField(blank=True)                # New

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobcard_id} - {self.trainset.number}"
class Mileage(models.Model):
    trainset = models.ForeignKey(Trainset, on_delete=models.CASCADE, related_name="mileages")

    last_mileage = models.IntegerField(default=0)
    cumulative_mileage = models.IntegerField(default=0)

    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mileage for {self.trainset.number}"

class Branding(models.Model):
    name = models.CharField(max_length=128)   # advertiser
    required_exposure_hours = models.IntegerField(default=0)
    achieved_hours = models.IntegerField(default=0)

class Bay(models.Model):
    name = models.CharField(max_length=64)
    position = models.IntegerField()  # numeric order for shunting minimization
    capacity = models.IntegerField(default=1)

class CleaningSlot(models.Model):
    bay = models.ForeignKey(Bay, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    assigned_trainset = models.ForeignKey(Trainset, null=True, blank=True, on_delete=models.SET_NULL)

class InductionDecision(models.Model):
    run_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    ranked_list = models.JSONField(blank=True,null=True)   # list of trains with reasons
    notes = models.TextField(blank=True)
