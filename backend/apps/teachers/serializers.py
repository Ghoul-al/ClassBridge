from rest_framework import serializers
from .models import Teacher, TeacherSubject, TeacherClass

class TeacherSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_name', 'department', 'employment_date', 'is_active']
        read_only_fields = ['id', 'employment_date']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)

class TeacherSubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_assigned.name', read_only=True)

    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name', 'class_assigned', 'class_name', 'assigned_date']
        read_only_fields = ['id', 'assigned_date']

class TeacherClassSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    class_name = serializers.CharField(source='class_assigned.name', read_only=True)

    class Meta:
        model = TeacherClass
        fields = ['id', 'teacher', 'teacher_name', 'class_assigned', 'class_name', 'role', 'assigned_date']
        read_only_fields = ['id', 'assigned_date']