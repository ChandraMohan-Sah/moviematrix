# serializers.py
from rest_framework import serializers
from user_profile.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = ['profile_pic']



class CompleteUserProfileInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta: 
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'date_joined',
            'profile_pic'
        ]

