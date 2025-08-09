from rest_framework import serializers
from django.core.validators import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        password = serializers.CharField(max_length=15)
        confirm_password = serializers.CharField(max_length=15)
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'age', 'password']


    def validate(self, data):
        confirm_password = self.initial_data.get('confirm_password')
        if data['password'] != confirm_password:
            raise ValidationError({'message':'parollar mos emas', 'status':status.HTTP_400_BAD_REQUEST})
        username = data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError({'message':"bu username orqali ro'yxtadan o'tilgan" , 'status':status.HTTP_400_BAD_REQUEST})
        return data

    def create(self, validated_data):
        # validated_data.pop('confirm_password')
        user = CustomUser.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            age = validated_data['age'],
            address = validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user