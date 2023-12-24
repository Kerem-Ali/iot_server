from rest_framework import serializers
from django.contrib.auth.models import User
from lights.models import Light
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id","username","password","email"]
        

class LightSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    ip = serializers.CharField()
    is_on = serializers.BooleanField()
    is_active = serializers.BooleanField(default=False)
    
    creation_date = serializers.DateTimeField(default=datetime.now())
    last_communication_date = serializers.DateTimeField(default=datetime.now())

    
    def create(self, validated_data):
        return Light.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.is_on = validated_data.get("is_on", instance.is_on)
        instance.last_communication_date = datetime.now()
        instance.save()
        return instance