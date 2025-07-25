# serializers.py
from django.contrib.auth.models import User 
from rest_framework import serializers 

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={
            'input_type':'password'
        },
        write_only=True
    )

    class Meta: 
        model = User 
        fields = (
            'username',
            'email',
            'password',
            'confirm_password'
        )

        extra_kwargs = {
            'password': {'write_only': True},
        }

    
    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError("Password do not match")
        
        user_queryset = User.objects.filter(
            email=self.validated_data['email']   
        )

        if user_queryset.exists():
            raise serializers.ValidationError("Email already exists")
        
        account = User(email=self.validated_data['email'],
                       username=self.validated_data['username'])
        
        account.set_password(password)
        account.save()
        return account 
    
