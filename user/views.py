from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service.onboarding_services import create_user_and_wallet
from user.serializer import UserSerializer, LoginSerializer


# Create your views here.
@api_view(['Post'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user,wallet = create_user_and_wallet(serializer.validated_data)
    return Response({"message" : "Registration Successful"},status.HTTP_201_CREATED)

@api_view(['Post'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data,status.HTTP_200_OK)