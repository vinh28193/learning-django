from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True, source="get_fullname")

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'fullname',
            'phone',
            'email',
            'avatar_image',
            'language',
            'timezone',
            'is_staff',
            'is_active',
        )
