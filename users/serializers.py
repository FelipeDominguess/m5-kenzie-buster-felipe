from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=127, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'birthdate', 'is_employee', 'is_superuser']
        read_only_fields = ['is_superuser']
        extra_kwargs = {
            'username': {
                'validators': [UniqueValidator(queryset=User.objects.all(), message="username already taken.")]
            },
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all(), message="email already registered.")]
            },
            'password': {'write_only': True},
        }

    def validate(self, data):
        is_superuser = data.get("is_superuser", False)

        if is_superuser:
            raise serializers.ValidationError("usuário comum deve ter is_superuser=False")

        return data

    def create(self, validated_data):
        is_superuser = validated_data.pop("is_superuser", False)

        if not is_superuser:
            validated_data["is_superuser"] = True

        instance = User.objects.create_user(**validated_data)

        return instance

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance
