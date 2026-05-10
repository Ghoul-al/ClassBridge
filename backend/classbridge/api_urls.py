from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.auth.urls')),
    # path('schools/', include('apps.schools.urls')),
    # Add other app URLs here
]