
from dataclasses import fields
from unittest import TextTestRunner
from rest_framework import serializers,exceptions
from api.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation, authenticate
from rest_framework.response import Response


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
    # complaint_file = image = Base64ImageField(
    #     max_length=None, use_url=True,
    # )
    class Meta:
        model = Complain
        fields = ['id','complaint_subject','complaint_details','complaint_file','state','complaint_category','complaint_sub_category','user_id','complaint_date','updation_date','complaint_status']

        extra_kwargs = {
                'complaint_date':{
                    'read_only':True
                },
                'updation_date':{
                    'read_only':True
                },
                'id':{
                    'read_only':True
                },
                'complaint_status':{
                    'read_only':True
                },
        }
    


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ User registration serializer class """
   
    username = serializers.CharField(required=True,help_text="Enter your Username.")
    email = serializers.EmailField(required=True,help_text="Enter your Email.")
    first_name = serializers.CharField(required=True,help_text="Enter your Firstname.")
    last_name = serializers.CharField(required=True,help_text="Enter your Lastname.")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'},help_text="Enter your Password.")

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password','is_active','created','is_superuser']
    
        extra_kwargs = {
                'is_active':{
                    'read_only':True
                },
                'is_superuser':{
                    'read_only':True
                },
                'created':{
                    'read_only':True,
                    'format':'%Y-%m-%d',
                },
        }

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

    def get_user_email(self,email):
        return email


    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = make_password(validated_data.get('password')),
        )
        return user

        # fields = ('id','username','email','password','first_name','last_name','contact_no','address','pincode','user_type','user_image','country_id','state_id')
        
        
        # extra_kwargs = {
        #     'contact_no':{
        #         'read_only':True
        #     },
        #     'address':{
        #         'read_only':True
        #     },
        #     'pincode':{
        #         'read_only':True
        #     },
        #     'user_image':{
        #         'read_only':True
        #     },
        #     'country_id':{
        #         'read_only':True
        #     },
        #     'state_id':{
        #         'read_only':True
        #     }
        # }

class ProfileSerializer(serializers.ModelSerializer):
    """ User Profile Serializer """
    # userData = UserRegistrationSerializer(read_only = True)
    user_image = serializers.ImageField(max_length=None,use_url=True,)
    class Meta:
        model = UserProfile
        fields = ('id','contact_no','address','pincode','gender','user_image','country','state','user',)

    def create(self, validated_data):
        profile = UserProfile.objects.create(
            contact_no = validated_data['contact_no'],
            address = validated_data['address'],
            pincode = validated_data['pincode'],
            gender = validated_data['gender'],
            user_image = validated_data['user_image'],
            country = validated_data['country'],
            state = validated_data['state'],
            user = validated_data['user'],
        )
       
        return profile

class UserApprovalSerializer(serializers.ModelSerializer):
    """ User Approval Serializer """

    is_active = serializers.BooleanField(required=True)
    
    class Meta:
        model =  User
        # exclude = ['username','email','password']
        fields = ('id','is_active','username','first_name','last_name','email')
        extra_kwargs = {
            'username':{
                'read_only':True
            },
            'first_name':{
                'read_only':True
            },
            'last_name':{
                'read_only':True
            },
            'email':{
                'read_only':True
            },
        }

    def update(self, instance, validated_data):
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username','password')
        def validate(self,data):
            user = authenticate(**data)
            if user:
                if user.is_active:
                    data['user'] = user
                    return data
                raise exceptions.AuthenticationFailed('Account is not activated')
            raise exceptions.AuthenticationFailed()


class ChangePasswordSerializer(serializers.ModelSerializer):
    """ Password Change serializer class """
    new_password = serializers.CharField(write_only=True,required=True,validators=[password_validation.validate_password])
    conf_password = serializers.CharField(write_only=True,required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password','new_password','conf_password')

    def validate(self,attrs):
        if attrs['new_password'] != attrs['conf_password']:
            raise serializers.ValidationError({"password":"Password fields doesn't match."})
        return attrs

    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password":"Old password is not correct"})
        return value

    def update(self,instance,validate_data):
        instance.set_password(validate_data['new_password'])
        instance.save()

        return instance


class ComplaintRemarksSerializer(serializers.ModelSerializer):
    """ Complaint remarks serializers """
    class Meta:
        model = ComplaintRemarks
        fields = '__all__'
        extra_kwargs = {
                'remarks_date':{
                    'read_only':True,
                    'format':'%Y-%m-%d %H:%M:%S',
                }
        }


class ComplaintStatusUpdateSerializer(serializers.ModelSerializer):
    """ Serializer class for updating only complaint status """   
    complaint_status = serializers.CharField(required=True)
    class Meta:
        model = Complain
        fields = ['id','complaint_subject','complaint_details','complaint_file','state','complaint_category','complaint_sub_category','user_id','complaint_date','updation_date','complaint_status']

        extra_kwargs = {
                'complaint_date':{
                    'read_only':True
                },
                'updation_date':{
                    'read_only':True
                },
                'user_id':{
                    'read_only':True
                },
                'complaint_subject':{
                    'read_only':True
                },
                'complaint_details':{
                    'read_only':True
                },
                'complaint_file':{
                    'read_only':True
                },
                'state':{
                    'read_only':True
                },
                'complaint_category':{
                    'read_only':True
                },
                'complaint_sub_category':{
                    'read_only':True
                },
        }
     


class FeedbackSerializer(serializers.ModelSerializer):
    """ feedback serializer class """
    class Meta:
        model = Feedback
        fields = '__all__'
        extra_kwargs = {
            'is_delete':{
                'read_only':True
            },
            'is_reg_user':{
                'read_only':True
            },
            'reg_date':{
                'format':'%Y-%m-%d %H:%M:%S',
            }
            
        }


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

