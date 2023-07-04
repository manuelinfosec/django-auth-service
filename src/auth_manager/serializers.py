from rest_framework import serializers
from django.contrib.auth import get_user_model

# Returns default Django user model from models.User
UserModel = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    # Specifies that password is accepted, but not written back
    password = serializers.CharField(write_only=True)

    def create(self, data):
        """Method is overridden to allow for custom 'create_user' call"""
        
        # Allows for creating user instances with hashed passwords
        user = UserModel.objects.create_user(
            username = data["username"],
            password = data["password"],
        )

        return user
    
    class Meta:
        model = UserModel
        fields = ("username", "first_name", "last_name", "password", )

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("first_name", "last_name",)