from rest_framework import serializers

from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email',"password","phone","username"]

        extra_kwargs = {
            "password": {"write_only":True}
        }

class LoginSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(max_length=30)
    def validate(self,data):
        email=data.get("email")
        password=data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid Credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account is not active")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid Credentials")

        refresh = RefreshToken.for_user(user)
        data = {
            "user" : user.id,
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
        }
        return data


    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     Wallet.objects.create(
    #         user=user,
    #         wallet_number=user.phone[1:]
    #     )
    #     return user