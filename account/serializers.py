from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'first_name','last_name','phone_number', 'address', 'gender','registration_date','last_login_date','role']
        read_only_fields = ['registration_date', 'last_login_date']

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name','last_name','phone_number', 'address', 'gender','last_login_date','registration_date','role']

    def save(self):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        first_name = self.validated_data.get('first_name', '')
        last_name = self.validated_data.get('last_name', '')
        phone_number = self.validated_data.get('phone_number', '')
        address = self.validated_data.get('address', '')
        gender = self.validated_data.get('gender', '')
        role= self.validated_data.get('role', 'generaluser')

        if password != password2:
            raise serializers.ValidationError({'error': "Passwords do not match"})
        if Account.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})

        account = Account(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            role=role,
        )
        account.set_password(password)
        account.is_active = False
        account.save()
        return account

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
