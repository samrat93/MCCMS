from click import style
from rest_framework import serializers
from api.models import *



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'


class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint_Category
        fields = '__all__'

    
class ComplaintSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint_Sub_Category
        fields = '__all__'
    


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'



class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id','username','email','user_type','password']
        extra_kwargs = {
            'password': {'write_only': True},
        }



# class UserRegistrationSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField()
#     confirm_password = serializers.CharField()

#     def validate_email(self, email):
#         existing = UserData.objects.filter(email=email).first()
#         if existing:
#             raise serializers.ValidationError('Someone with that email has already exist')
#         return email

#     def validate(self, data):
#         if not data.get('password') or not data.get('confirm_password'):
#             raise serializers.ValidationError('Please enter a password and confirm it.')
#         if data.get('password') != data.get('confirm_password'):
#             raise serializers.ValidationError('Password Doesnot match.')
#         return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = UserData
        fields = ['username','email','user_type','password','password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        userdata = UserData(
            email = self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data(['password'])
        password2 = self.validated_data('password2')

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match.'})
        userdata.set_password(password)
        userdata.save()
        return userdata