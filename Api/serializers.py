from rest_framework import serializers

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()
    
from rest_framework import serializers
from .models import ErrorReport

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = ['code', 'description', 'date']