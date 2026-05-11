from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(school_id=self.request.school_id)
        return queryset