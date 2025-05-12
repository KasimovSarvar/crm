from django.contrib.auth import authenticate
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from  rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from lead.models import Lead, Student
from .models import User
from lead.serialazer import LeadSerializer,StudentSerializer
from .serialazer import UserSerializer



@api_view(['GET'])
def home_view(request):
    return Response(data={"ok":request.user.username}, status=status.HTTP_200_OK)



@swagger_auto_schema(methods=['POST'],responses={200:UserSerializer(many=True)})
@api_view(http_method_names=['POST'])
def register_view(request):
    if request.user.role != 1: #4
        return Response(data={"Error":"Only super user can create new user"},status=status.HTTP_400_BAD_REQUEST)

    serial= UserSerializer(data=request.data)
    if  not serial.is_valid():
        return Response(data=serial.errors, status=status.HTTP_400_BAD_REQUEST)



    user_obj = serial.save()
    user_obj.set_password(user_obj.password)
    user_obj.save()

    if user_obj.role == 1: #3
        return Response(data={"NONE": "Super user only admin panel create "}, status=status.HTTP_400_BAD_REQUEST)



    return Response(data={"ok":user_obj.username}, status=status.HTTP_200_OK)





@api_view(['POST'])
def login_view(request):
    username = request.data["username"]
    password = request.data["password"]

    auth = authenticate(request,username=username, password=password)
    if auth is None:
        return Response(data={"NONE":"Username or passsword is inncorrect"}, status=status.HTTP_400_BAD_REQUEST)


    refresh_token = RefreshToken.for_user(auth)
    access_token = refresh_token.access_token

    return Response(data={"access_token":str(access_token),"refresh_token":str(refresh_token)},status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['GET'],responses={200:UserSerializer(many=True)})
@api_view(['GET'])
def control_user_view(request):
    if request.user.role == 1:
        user_obj = User.objects.all()
        return Response(data=UserSerializer(user_obj,many=True).data, status=status.HTTP_200_OK)
    return Response(data={"Error":"Only super user"}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET'],responses={200:LeadSerializer(many=True)})
@api_view(['GET'])
def control_lead_view(request):
    if request.user.role == 1:
        lead_obj = Lead.objects.all()
        return Response(data=LeadSerializer(lead_obj,many=True).data, status=status.HTTP_200_OK)
    return Response(data={"Error":"Only super user"}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['GET'],responses={200:StudentSerializer(many=True)})
@api_view(['GET'])
def control_student_view(request):
    if request.user.role == 1:
        student_obj = Student.objects.all()
        return Response(data=StudentSerializer(student_obj,many=True).data, status=status.HTTP_200_OK)
    return Response(data={"Error":"Only super user"}, status=status.HTTP_200_OK)