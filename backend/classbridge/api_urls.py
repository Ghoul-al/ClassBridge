from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.auth.urls')),
    path('schools/', include('apps.schools.urls')),
    path('classes/', include('apps.classes.urls')),
    path('subjects/', include('apps.subjects.urls')),
    path('academic/', include('apps.academic.urls')),
    path('students/', include('apps.students.urls')),
    path('teachers/', include('apps.teachers.urls')),
    path('parents/', include('apps.parents.urls')),
    path('learning/', include('apps.learning.urls')),
    path('cbt/', include('apps.cbt.urls')),
    # Add other app URLs here
]