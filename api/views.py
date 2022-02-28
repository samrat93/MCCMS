
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import *
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view



# Create your views here.

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


# class UserDataApiViewSet(viewsets.ModelViewSet):
#     serializer_class = UserDataSerializer
#     queryset = UserData.objects.all()
#     permission_classes = [permissions.IsAdminUser]


# class UserRegistrationViewSet(viewsets.ModelViewSet):
#     queryset = UserData.objects.all()
#     serializer_class = UserDataSerializer

#     @action(detail=True,methods=['post'],permission_classes=[AllowAny])
#     def register(self,request):
#         serializer = UserRegistrationSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)

#         model_serializer = UserDataSerializer(data = serializer.data)
#         model_serializer.is_valid(raise_exception=True)
#         model_serializer.save()

#         return Response(model_serializer.data)

#     @action(detail=True,methods=['get'])
#     def info(self,request):
#         serializer = UserDataSerializer(request.user)
#         return Response(serializer.data)

#     def list(self,request):
#         user = request.user
#         if not user or not user.is_superuser:
#             return HttpResponseForbidden()
#         return super(UserRegistrationViewSet,self).list(request)

#     def update(self,request,pk=None):
#         user = UserData.objects.filter(id=pk).first()
#         if not user or request.user != user:
#             return HttpResponseForbidden()
#         return super(UserRegistrationViewSet,self).update(request)

# def UserRegistrationViewSet(viewsets.ModelViewSet):


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            userdata = serializer.save()
            data['response'] = 'successfully registered a new user'
            data['email'] = userdata.email
            data['username'] = userdata.username
        else:
            data = serializer.errors
        return Response(data)

