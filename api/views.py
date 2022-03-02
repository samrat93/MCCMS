
from tokenize import Token
from django import views
from rest_framework import viewsets
from api.models import *
from .serializers import *
from rest_framework import permissions
from .permission import UpdateOwnProfile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings


# Create your views here.

class UserLoginApiView(ObtainAuthToken):
    """ Django login for tokan authentication """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class StateApiViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    permission_classes = [permissions.IsAdminUser]


class CountryApiViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    permission_classes = [permissions.IsAdminUser]


class MunicipalityApiViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipalitySerializer
    queryset = Municipality.objects.all()
    permission_classes = [permissions.IsAdminUser]


class ComplaintCategoryApiViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintCategorySerializer
    queryset = Complaint_Category.objects.all()
    permission_classes = [permissions.IsAdminUser]


class ComplaintSubCategoryApiViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSubCategorySerializer
    queryset = Complaint_Sub_Category.objects.all()
    permission_classes = [permissions.IsAdminUser]


class ComplaintApiViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    queryset = Complain.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserProfileApiViewSet(viewsets.ModelViewSet):
    serializer_class = userProfileSerializer
    queryset = UserProfile.objects.all()
    # authentication_class = (TokenAuthentication)
    permission_classes = [UpdateOwnProfile]




class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    authentication_class = (TokenAuthentication)
    permission_classes = [UpdateOwnProfile]





