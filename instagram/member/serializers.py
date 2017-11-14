from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = (
            'pk',
            'username',
            'img_profile',
            'age',
        )


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'img_profile',
            'username',
            'password1',
            'password2',
            'age',
            # 'token',
        )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        # return self.Meta.objects.create_user(
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            age=validated_data['age'],
        )

    # @staticmethod
    # def get_token(obj):
    #     return Token.objects.create(user=obj).key
    def to_representation(self, instance):
        # serializer된 형태를 결정
        # super().to_representation()은 serialize된 기본 형태(dict)
        ret = super().to_representation(instance)
        data = {
            'user': ret,
            'token': instance.token,
        }
        # 마지막엔 serializer.data를 출력했을 때 반환될 값을 반환해줘야 함
        return data
