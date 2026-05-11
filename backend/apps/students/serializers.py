from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class_name = serializers.CharField(source='class_assigned.name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'user_name', 'class_assigned', 'class_name', 'admission_number', 'gender', 'date_of_birth', 'enrollment_date', 'is_active']
        read_only_fields = ['id', 'enrollment_date']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)