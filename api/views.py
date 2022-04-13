
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
from rest_framework import generics, permissions,status
from .myPaginations import MyPageNumberPagination
from .utils import Util


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
                    'first_name':user.first_name,
                    'last_name':user.last_name,
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
    permission_classes = [permissions.IsAuthenticated]


class ComplaintSubCategoryApiViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSubCategorySerializer
    queryset = Complaint_Sub_Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ComplaintApiViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    queryset = Complain.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # def perform_create(self, serializer):
    #     complaint_file = self.request.FILES['complaint_file']
    #     return super().perform_create(serializer)


class UserProfileApiViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_class = (TokenAuthentication)
    permission_classes = [UpdateOwnProfile]



class UserRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.filter(is_superuser=False)
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.AllowAny]
    pagination_class = MyPageNumberPagination




class UserApprovalAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserApprovalSerializer
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAdminUser]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            email_body = 'Hello '+user.username + \
                ' Congratulations 😊 Your account is activated. You can now login to your system.'
            data = {'email_body':email_body,'to_email':user.email,'email_subject':'Account Activation'}
            Util.send_email(data)
            return Response({"message":"User is activated successfully"})
        else:
            return Response({"message": "failed", "details": serializer.errors})

       


class ChangePasswordView(generics.UpdateAPIView):
    """ Password change view class """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAuthenticated]
    

class ComplaintRemarksViewSet(viewsets.ModelViewSet):
    """ Complaint Remarks Adding view class """
    queryset = ComplaintRemarks.objects.all()
    serializer_class = ComplaintRemarksSerializer
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAuthenticated]


class ComplaintRemarksUpdateViewSet(generics.UpdateAPIView):
    """ Complaint Remarks update view """
    queryset = Complain.objects.all()
    serializer_class = ComplaintStatusUpdateSerializer
    authentication_class = (TokenAuthentication)
    permission_classes = [permissions.IsAdminUser]



class FeedbackApiView(generics.GenericAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        email_body = 'Hello '+user.username + \
            ' Thank you for your valuable feedback.'
        data = {'email_body':email_body,'to_email':user.email,'email_subject':'Feedback'}
        Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)

    def get(self,request,format=None):
        feedbacks = Feedback.objects.all() 
        serializer = FeedbackSerializer(feedbacks,many=True)
        return Response(serializer.data)


class ForgetPasswordView(generics.GenericAPIView):
    """ Forget password view class """
    serializer_class = ForgetPasswordSerializer

    def get_queryset(self):
        queryset = User.objects.get(id=self.kwargs['id'])
        email_body = 'Hello '+queryset.username + \
            ' Thank you for your valuable feedback.'
        data = {'email_body':email_body,'to_email':queryset.email,'email_subject':'Feedback'}
        Util.send_email(data)





class UserListOnlyViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    authentication_class = (TokenAuthentication)
    # permission_classes = [permissions.IsAuthenticated]

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = ListUserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    
    
    
# class RequestPasswordResetEmail(generics.GenericAPIView):
#     """ Request password reset email """
#     serializer_class = ResetPasswordEmailRequestSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)

#         email = request.data.get('email', '')

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(
#                 request=request).domain
#             relativeLink = reverse(
#                 'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

#             redirect_url = request.data.get('redirect_url', '')
#             absurl = 'http://'+current_site + relativeLink
#             email_body = 'Hello, \n Use link below to reset your password  \n' + \
#                 absurl+"?redirect_url="+redirect_url
#             data = {'email_body': email_body, 'to_email': user.email,
#                     'email_subject': 'Reset your passsword'}
#             Util.send_email(data)
#         return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)




