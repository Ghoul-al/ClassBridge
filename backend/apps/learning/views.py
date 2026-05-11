from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import Assignment, AssignmentSubmission, FileUpload
from .serializers import AssignmentSerializer, AssignmentSubmissionSerializer, FileUploadSerializer
from .utils import upload_file_to_minio

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(school_id=self.request.school_id)
        return queryset

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(assignment__school_id=self.request.school_id)
        return queryset

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        submission = self.get_object()
        if submission.student.user != request.user and request.user.role not in ['teacher', 'school_admin']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        submission.status = 'submitted'
        submission.submitted_at = timezone.now()
        submission.save()
        serializer = self.get_serializer(submission)
        return Response(serializer.data)

class FileUploadViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['post'])
    def upload(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        file_name = file_obj.name

        # Basic validation
        if file_obj.size > 10 * 1024 * 1024:  # 10MB limit
            return Response({'error': 'File too large'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'image/jpeg', 'image/png', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']
        if file_obj.content_type not in allowed_types:
            return Response({'error': 'File type not allowed'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_upload = upload_file_to_minio(file_obj, file_name, request.school_id, request.user)
            serializer = FileUploadSerializer(file_upload)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)