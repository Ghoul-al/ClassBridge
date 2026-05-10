from rest_framework import viewsets
from .models import Subject
from .serializers import SubjectSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(school_id=self.request.school_id)
        return queryset