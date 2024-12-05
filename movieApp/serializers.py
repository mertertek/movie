from rest_framework import serializers
from .models import CustomUser, Movie, Comment, Favorite, Category
from datetime import date
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'movie', 'user', 'rating', 'comment', 'is_public']
        read_only_fields = ['user', 'movie']

    def validate_rating(self, value):
        
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = Category
        fields = "__all__"

class UserRegisterationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "password")

    def create(self, validated_date):
            return CustomUser.objects.create_user(**validated_date)

class UserLoginSeriazlier(serializers.ModelSerializer):
    
    email =serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = "__all__"