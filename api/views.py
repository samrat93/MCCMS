

from rest_framework import viewsets
from api.models import *
from .serializers import *
from rest_framework import permissions
from .permission import UpdateOwnProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from knox.views import LoginView
from knox.auth import AuthToken
from rest_framework import generics, permissions
from rest_framework import status

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
                    'email':user.email,
                    'is_superuser':user.is_superuser,
            },
            'token':token
        })
        # login(request,user)
        # return super(LoginUserView,self ).post(request)


class StateApiViewSet(viewsets.ModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAuthenticated]


class CountryApiViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAuthenticated]


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
    authentication_class = (TokenAuthentication)
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


class ChangePasswordView(generics.UpdateAPIView):
    """ Password change view class """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAuthenticated]
    

    # def get_object(self,queryset=None):
    #     obj = self.request.user
    #     return obj

    # def update(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     serializer = self.get_serializer(data = request.data)

    #     if serializer.is_valid():
    #         # checking old password
    #         if not self.object.check_password(serializer.data.get("old_password")):
    #             return Response({"old_password": ["Old password is incorrect."]}, status=status.HTTP_400_BAD_REQUEST)
            
    #         self.object.set_password(serializer.data.get('new_password'))
    #         self.object.save()
    #         response = {
    #             'status': 'success',
    #             'code': status.HTTP_200_OK,
    #             'message': 'Password updated successfully',
    #             'data': []
    #         }
    #         return Response(response)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    





