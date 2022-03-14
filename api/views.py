
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from api.models import *
from .serializers import *
from rest_framework import permissions
from .permission import UpdateOwnProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from knox.views import LoginView
from knox.auth import AuthToken
from rest_framework import generics, mixins, permissions

# from rest_framework.authtoken.views import ObtainAuthToken
# from tokenize import Token
# from django.contrib.auth import login
# from rest_framework.settings import api_settings


# Create your views here.

# class UserLoginApiView(ObtainAuthToken):
#     """ Django login for tokan authentication """

#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class LoginUserView(LoginView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        serializer = AuthTokenSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        _, token = AuthToken.objects.create(user)
        return Response({
            'user_Info':{
                    'id':user.id,
                    'username':user.username,
                    'email':user.email
            },
            'token':token
        })
        # login(request,user)
        # return super(LoginUserView,self ).post(request)


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
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_class = (TokenAuthentication)
    permission_classes = [UpdateOwnProfile]




class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    authentication_class = (TokenAuthentication)
    permission_classes = [UpdateOwnProfile]


class UserApprovalAPIView(generics.UpdateAPIView):
    serializer_class = UserApprovalSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    

    # parser_classes = (MultiPartParser, FormParser,)
    # def get_object(self):
    #     is_active = self.kwargs["is_active"]
    #     obj = get_object_or_404(User,is_active=is_active)
    #     return obj

    # # def delete(self,request,*args,**kwargs):
    # #     return self.destroy(request,*args, **kwargs)

    # def put(self,request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)







