from rest_framework import viewsets
from .models import Parent, ParentStudent
from .serializers import ParentSerializer, ParentStudentSerializer

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(school_id=self.request.school_id)
        return queryset

class ParentStudentViewSet(viewsets.ModelViewSet):
    queryset = ParentStudent.objects.all()
    serializer_class = ParentStudentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(parent__school_id=self.request.school_id)
        return queryset