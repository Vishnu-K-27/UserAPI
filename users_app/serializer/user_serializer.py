from rest_framework import serializers
from users_app.model.users import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"