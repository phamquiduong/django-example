from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)

    class Meta:
        model = UserModel
        fields = ("id", "email", "password", "last_login", "date_joined", "is_active")
