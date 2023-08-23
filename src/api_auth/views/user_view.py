from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from api_auth.serializers.user_serializer import UserSerializer

UserModel = get_user_model()


class CreateUserView(CreateAPIView):
    model = UserModel
    serializer_class = UserSerializer
