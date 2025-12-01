from django import forms
from .models import (
    Trainset,
    JobCard,
    Branding,
    Bay,
    FitnessCertificate,
    CleaningSlot,
    InductionDecision,
    Mileage,
)


class AddTrainForm(forms.ModelForm):
    class Meta:
        model = Trainset
        # user wanted only number, cars and notes on add page
        fields = ['number','train_name', 'cars', 'notes']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'TS-01'}),
            'train_name': forms.TextInput(attrs={'placeholder': 'Aluva Shuttle'}),

            'cars': forms.NumberInput(),
            'notes': forms.Textarea(attrs={'rows':2}),
        }

class FitnessDetailForm(forms.ModelForm):
    class Meta:
        model = FitnessCertificate
        fields = ['department', 'valid_from', 'valid_to', 'doc']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class JobCardDetailForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ['jobcard_id', 'assigned_task', 'status',
                  'last_service_date', 'next_maintenance_date',
                  'operator', 'remarks']
        widgets = {
            'last_service_date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BrandingDetailForm(forms.ModelForm):
    class Meta:
        model = Branding
        fields = ['name', 'required_exposure_hours', 'achieved_hours']

class MileageDetailForm(forms.ModelForm):
    # We'll update Trainset mileage directly so use Trainset model here
    class Meta:
        model = Mileage
        fields = ['last_mileage', 'cumulative_mileage']

class CleaningDetailForm(forms.ModelForm):
    class Meta:
        model = CleaningSlot
        fields = ['bay', 'start_time', 'end_time', 'assigned_trainset']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class GeometryDetailForm(forms.ModelForm):
    class Meta:
        model = Bay
        fields = ['name', 'position', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Bay A',
                'class': 'form-control'
            }),
            'position': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }

# -----------------------------
# Induction Decision Form
# -----------------------------
class InductionDecisionForm(forms.ModelForm):
    class Meta:
        model = InductionDecision
        fields = [
            "run_date",
            "ranked_list",
            "notes",
        ]
