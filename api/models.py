from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
# from django.contrib.auth.models import User


# Create your models here.



class State(models.Model):
    """ Modal for state table"""
    state_name = models.CharField(max_length=40,unique=True)
    state_desc = models.CharField(max_length=1000,null=True,blank=True)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.state_name

class Country(models.Model):
    country_name = models.CharField(max_length=40,unique=True)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    country_desc = models.CharField(max_length=1000,null=True,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.country_name


class Municipality(models.Model):
    """ This is the model of Municipality """

    municipality_name = models.CharField(max_length=100)
    municipality_address = models.CharField(max_length=500)
    is_verified = models.BooleanField(default=False)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    municipality_desc = models.TextField(blank=True,null=True)
    phone_regex = RegexValidator(regex="^(\+\d{1,3})?,?\s?\d{8,13}")
    contact_no = models.CharField(validators=[phone_regex], verbose_name=("Contact Number"),max_length=17, blank=True,null=True)
    pincode = models.CharField(max_length=6,blank=True,null= True)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)


    def __str__(self):
        return self.municipality_name


class CustomAccountManager(BaseUserManager):
    """ Custome User manager class for new user and superuser """

    def create_superuser(self, email, username, first_name,last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name,last_name, password, **other_fields)

    def create_user(self, email, username, first_name,last_name, password, **other_fields):

        if not email:
            raise ValueError(('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name,last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model to add extra field in django table """

    objects = CustomAccountManager()
    username = models.CharField(max_length=150,unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'email','first_name','last_name']

    def __str__(self):
        return self.username
    

class UserProfile(models.Model):

    USER_TYPE = (
        ('P', 'Public'),
        ('M','Municipality'),
    )
    GENDER = (
        ('M','Male'),
        ('F','Female'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex="^(\+\d{1,3})?,?\s?\d{8,13}")
    contact_no = models.CharField(validators=[phone_regex], verbose_name=("Mobile Number"),max_length=17, blank=True,null=True)
    address = models.CharField(max_length=1024, blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    pincode = models.CharField(max_length=6,blank=True,null= True)
    gender = models.CharField(max_length=1,choices=GENDER)
    user_image = models.ImageField(null=True,blank=True)
    user_type = models.CharField(max_length=12,choices=USER_TYPE,default='P',null= True,blank=True)

    def __unicode__(self):
        return u'Profile of user:{0}'.format(self.user.email)
    def __str__(self):
        return self.user.username




class Complaint_Category(models.Model):
    """ Complaint category table """

    category_name = models.CharField(max_length=100,unique=True)
    category_desc = models.CharField(max_length=1000,null=True,blank=True)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.category_name


class Complaint_Sub_Category(models.Model):
    """ Sub category of complaint_category table """
    sub_category_name = models.CharField(max_length=100,unique=True)
    sub_category_desc = models.CharField(max_length=1000,null=True,blank=True)
    category_id = models.ForeignKey(Complaint_Category,on_delete=models.CASCADE)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.sub_category_name


class Complain(models.Model):
    """ This is for Complain table """
    status = (
        ('1','Pending'),
        ('2','Processing'),
        ('3','Closed'),
    )

    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    complaint_category = models.ForeignKey(Complaint_Category,on_delete=models.CASCADE)
    complaint_sub_category = models.ForeignKey(Complaint_Sub_Category,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality,on_delete=models.CASCADE,blank=True,null=True)
    complaint_subject = models.CharField(max_length=500,blank=True,null=True)
    complaint_details = models.TextField(blank=True)
    complaint_file = models.ImageField(null=True,blank=True)
    complaint_status = models.CharField(max_length=10, choices=status,default=1)
    complaint_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.complaint_subject
    # def image_img(self):
    #     if self.complaint_file:
    #         return u'<img src="%s"width="50" height="50"/>'%self.complaint_file.url
    #     else:
    #         return '(Sin imagen)'
    #     image_img.short_description ='Thumb'
    #     image_img.allow_tags =True
    
