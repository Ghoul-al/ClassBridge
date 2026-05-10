from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.auth.urls')),
    path('schools/', include('apps.schools.urls')),
    path('classes/', include('apps.classes.urls')),
    path('subjects/', include('apps.subjects.urls')),
    path('academic/', include('apps.academic.urls')),
    # Add other app URLs here
]