# depot/admin.py
from django.contrib import admin
from .models import Trainset, FitnessCertificate, JobCard, Branding, Bay, CleaningSlot, InductionDecision

@admin.register(Trainset)
class TrainsetAdmin(admin.ModelAdmin):
    list_display = ('number', 'cars', 'status', 'cumulative_mileage')
    search_fields = ('number',)

@admin.register(FitnessCertificate)
class FitnessCertAdmin(admin.ModelAdmin):
    list_display = ('trainset', 'department', 'valid_from', 'valid_to')

@admin.register(JobCard)
class JobCardAdmin(admin.ModelAdmin):
    list_display = (
        'jobcard_id',
        'assigned_task',
        'status',
        'last_service_date',
        'next_maintenance_date',
        'operator',
        'trainset',
    )

@admin.register(Branding)
class BrandingAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_exposure_hours', 'achieved_hours')

@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'capacity')

@admin.register(CleaningSlot)
class CleaningSlotAdmin(admin.ModelAdmin):
    list_display = ('bay', 'start_time', 'end_time', 'assigned_trainset')

@admin.register(InductionDecision)
class InductionDecisionAdmin(admin.ModelAdmin):
    list_display = ('run_date', 'created_at')
    readonly_fields = ('created_at',)
