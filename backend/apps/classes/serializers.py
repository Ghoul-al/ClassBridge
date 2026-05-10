from rest_framework import serializers
from .models import Section, Arm, Class

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)

class ArmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arm
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)

class ClassSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    arm_name = serializers.CharField(source='arm.name', read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'level', 'section', 'section_name', 'arm', 'arm_name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)