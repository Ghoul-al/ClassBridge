from rest_framework import viewsets
from .models import Teacher, TeacherSubject, TeacherClass
from .serializers import TeacherSerializer, TeacherSubjectSerializer, TeacherClassSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(school_id=self.request.school_id)
        return queryset

class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(teacher__school_id=self.request.school_id)
        return queryset

class TeacherClassViewSet(viewsets.ModelViewSet):
    queryset = TeacherClass.objects.all()
    serializer_class = TeacherClassSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(teacher__school_id=self.request.school_id)
        return queryset