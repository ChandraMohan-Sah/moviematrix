# serializers.py
from rest_framework import serializers
from user_profile.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = ['profile_pic']



class CompleteUserProfileInfoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'date_joined',
            'profile_pic'
        ]

