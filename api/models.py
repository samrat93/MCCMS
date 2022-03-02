from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


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



class UserProfile(models.Model):
    """ Custom user model to add extra field in django table """

    user_type = (
        ('1', 'Public'),
        ('2','Municipality'),
    )
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex="^(\+\d{1,3})?,?\s?\d{8,13}")
    contact_no = models.CharField(validators=[phone_regex], verbose_name=("Mobile Number"),max_length=17, blank=True,null=True)
    address = models.CharField(max_length=1024, blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    pincode = models.CharField(max_length=6,blank=True,null= True)
    user_type = models.CharField(max_length=12,choices=user_type,default=1,null= True,blank=True)
    user_image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.username
    


class Complaint_Category(models.Model):
    """ Complaint category table """

    category_name = models.CharField(max_length=100)
    category_desc = models.CharField(max_length=1000,null=True,blank=True)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.category_name


class Complaint_Sub_Category(models.Model):
    """ Sub category of complaint_category table """
    sub_category_name = models.CharField(max_length=100)
    sub_category_desc = models.CharField(max_length=1000,null=True,blank=True)
    category_id = models.ForeignKey(Complaint_Category,on_delete=models.CASCADE,blank=True,null=True)
    posting_date = models.DateField(auto_now_add=True,auto_now=False,blank=True)
    updation_date = models.DateField(auto_now_add=False, auto_now=True,blank=True)

    def __str__(self):
        return self.sub_category_name


class Complain(models.Model):
    """ This is for Complain table """
    status = (
        ('1','Pending'),
        ('2','Processing'),
        ('2','Closed'),
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
    
