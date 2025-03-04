from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from ..models import *
UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        user_obj = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user_obj

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('User not found')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'

class InstagramAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramAccount
        fields = ('username', 'password')

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    payment_history = PaymentHistorySerializer(many=True, read_only=True)
    instagram_accounts = InstagramAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'username',
            'user_id',
            'age',
            'has_confirmed_otp',
            'number_of_ig_accounts',
            'height',
            'stripe_customer_id',
            'subscription_plan',
            'subscription_end_date',
            'subscription_is_valid',
            'payment_history', 'instagram_accounts'
        ]