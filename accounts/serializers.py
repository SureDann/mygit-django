from . import models
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class GetUserSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = models.UserS
        fields = '__all__'


class RegisterSeriliazer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.UserS.objects.all())]

    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.UserS
        fields = ("username", "password", "password2", "email", "first_name", "last_name")
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},

        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didnt match"})

        return attrs

    def create(self, validated_data):
        user = models.UserS.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

# class TokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Token
#         fields = "__all__"

# class UserTokenSerializer(serializers.ModelSerializer):
#     tokens = TokenSerializer
#     class Meta:
#         model = models.UserS
#         fields = ["username", "password", "tokens"]


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserS
        fields = ("email", "password")

