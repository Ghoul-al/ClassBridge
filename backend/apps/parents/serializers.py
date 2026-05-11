from rest_framework import serializers
from .models import Parent, ParentStudent

class ParentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'user', 'user_name', 'relationship', 'phone', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)

class ParentStudentSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.user.get_full_name', read_only=True)
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)

    class Meta:
        model = ParentStudent
        fields = ['id', 'parent', 'parent_name', 'student', 'student_name', 'relationship', 'created_at']
        read_only_fields = ['id', 'created_at']