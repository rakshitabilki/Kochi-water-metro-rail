# kmrl/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('accounts.urls')),

# Home page (root)
    path('', include('home.urls', namespace='home')),

    # Keep the depot app under /depot/
    path('depot/', include('depot.urls', namespace='depot')),

    # Redirect root ('/') to the induction planner (change target if needed)
    path('', RedirectView.as_view(pattern_name='accounts:login', permanent=False)),
   
]

# During development serve static files (only when DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
