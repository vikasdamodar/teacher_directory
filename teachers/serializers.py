from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from teachers.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('subjects_taught') and len(validated_data.get('subjects_taught')) > 5:
            raise ValidationError("Teacher cannot teach more than 5 subjects.")
        data = super().create(validated_data)
        return data

    def update(self, instance, validated_data):
        if validated_data.get('subjects_taught') and len(validated_data.get('subjects_taught')) > 5:
            raise ValidationError("Teacher cannot teach more than 5 subjects.")
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['subjects'] = obj.subjects_taught.values_list('name', flat=True)
        del data['subjects_taught']
        return data


class TeacherQuerySerializer(serializers.Serializer):
    last_name = serializers.CharField(required=False, allow_null=True, help_text="Filter teachers by last_name")
    subject = serializers.CharField(required=False, allow_null=True, help_text="Filter teachers by a subject taught")
