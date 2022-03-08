from rest_framework import serializers
from api.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation, authenticate
# from django.utils.translation import ugettext_lazy as _


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



class UserRegistrationSerializer(serializers.ModelSerializer):
    """ User registration serializer class """
   
    username = serializers.CharField(help_text="Enter your Username.",write_only=True,)
    email = serializers.EmailField(required=True,help_text="Enter your Email.")
    first_name = serializers.CharField(required=True,help_text="Enter your Firstname.")
    last_name = serializers.CharField(required=True,help_text="Enter your Lastname.")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'},help_text="Enter your Password.")

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password']
        # extra_kwargs = {'email':{'validators':[]}}

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_email(self, email):
        """ Email Validation function """
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError('Someone with this email has already exist')
        return email

    def validate_username(self, username):
        """ Email Validation function """
        existing = User.objects.filter(username=username).first()
        if existing:
            raise serializers.ValidationError('Someone with this username has already exist')
        return username

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = make_password(validated_data.get('password')),
        )
        return user


class userProfileSerializer(serializers.ModelSerializer):
    """ Serializer for Userprofile """
    class Meta:
        model = UserProfile
        fields = ['id','contact_no','address','pincode','user_type','user_image','country_id','state_id','user_id']


# class LoginSerializers(serializers.Serializer):
#     username = serializers.CharField(max_length = 35)
#     password = serializers.CharField(
#         label=_("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         max_length=128,
#         write_only=True
#     )
#     def validate(self,data):
#         username = data.get('username')
#         password = data.get('password')
#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#             if not user:
#                 # msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError('Unable to log in with provided credentials.')
#             return  user
'''
class UserRegistrationSerializer(serializers.Serializer):
    type = (
        ('1', 'Public'),
        ('2','Municipality'),
    )
    username = serializers.CharField(help_text="Enter your Username.",write_only=True,)
    email = serializers.EmailField(required=True,help_text="Enter your Email.")
    first_name = serializers.CharField(required=True,help_text="Enter your Firstname.")
    last_name = serializers.CharField(required=True,help_text="Enter your Lastname.")
    address = serializers.CharField(required=True, help_text="Enter your Address.")
    user_type = serializers.ChoiceField(choices=type,default=1,help_text="Please select your user type.")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'},help_text="Enter your Password.")
    confirm_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'},help_text="Confirm your password.")

    def validate_email(self, email):
        existing = UserData.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError('Someone with that email has already exist')
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError('Please enter a password and confirm it.')
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Password Doesnot match.')
        return data

    def create(self, validated_data):
        user = UserData.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            user_type = validated_data['user_type'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            address = validated_data['address'],
            password = make_password(validated_data.get('password')),
        )
        return user

'''

# fields = ['id','username','first_name','last_name','email','date_joined','address','pincode','user_type','country_id','state_id']

