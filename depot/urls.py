from django.urls import path
from . import views

app_name = 'depot'

urlpatterns = [
    # Dashboard (main volunteer homepage)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Individual feature pages
    path('job-card-status/', views.job_card_status, name='job_card_status'),
    path('branding/', views.branding, name='branding'),
    path('fitness/', views.fitness, name='fitness'),
    path('mileage/', views.mileage, name='mileage'),
    path('cleaning/', views.cleaning, name='cleaning'),
    path('geometry/', views.geometry, name='geometry'),
    path('add-train/', views.add_train, name='add_train'),
    path('api/fitness/', views.api_fitness_data, name='api_fitness'),
    path("api/branding/", views.api_branding_data, name="api_branding"),
    path("api/jobcard/", views.api_jobcard_data, name="api_jobcard"),
    path("api/mileage/", views.api_mileage_data, name="api_mileage"),
    path("api/cleaning/", views.api_cleaning_data, name="api_cleaning"),
    path("api/geometry/", views.api_geometry_data, name="api_geometry"),
    path("schedule/ai/", views.induction_schedule_view, name="induction_schedule"),


    path('fitness/<str:number>/', views.fitness_detail, name='fitness_detail'),
    path('jobcard/<str:number>/', views.jobcard_detail, name='jobcard_detail'),
    path('branding/<str:number>/', views.branding_detail, name='branding_detail'),
    path('mileage/<str:number>/', views.mileage_detail, name='mileage_detail'),
    path('cleaning/<str:number>/', views.cleaning_detail, name='cleaning_detail'),
    path('geometry/<str:number>/', views.geometry_detail, name='geometry_detail'),







    # Default route (optional) — shows dashboard if /depot/ visited
    path('', views.dashboard, name='home'),
]
