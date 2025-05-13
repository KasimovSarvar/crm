from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from  rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from lead.models import Lead, Student,Payment,Outcome
from .models import User
from lead.serialazers import LeadSerializer,StudentSerializer,PaymentSerializer,OutcomeSerializer
from .serialazers import UserSerializer



@swagger_auto_schema(methods=['POST'],responses={200:UserSerializer(many=True)})
@api_view(['POST'])
def register_view(request):
    if request.user.role != 1:
        return Response(data={"Error":"Only super user can create new user"},status=status.HTTP_400_BAD_REQUEST)

    serial= UserSerializer(data=request.data)
    if  not serial.is_valid():
        return Response(data=serial.errors, status=status.HTTP_400_BAD_REQUEST)


    user_obj = serial.save()
    user_obj.set_password(user_obj.password)
    user_obj.save()

    if user_obj.role == 1:
        return Response(data={"NONE": "Super user only admin panel create "}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={"ok":user_obj.username}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    username = request.data["username"]
    password = request.data["password"]


    user_model = User.objects.filter(username=username).first()
    if not user_model:
        return Response(data={"Error":"Username not found"},status=status.HTTP_400_BAD_REQUEST)

    if not check_password(password,user_model.password):
        return Response(data={"Error":"Wrong password"},status=status.HTTP_400_BAD_REQUEST)


    refresh_token = RefreshToken.for_user(user_model)

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

  
@swagger_auto_schema(methods=['GET'],responses={200:PaymentSerializer(many=True)})
@api_view(['GET'])
def control_payment_view(request):
    if request.user.role == 1:
        payment_obj = Payment.objects.all()
        return Response(data=PaymentSerializer(payment_obj,many=True).data, status=status.HTTP_200_OK)
    return Response(data={"Error":"Only super user"}, status=status.HTTP_200_OK)

  
@swagger_auto_schema(methods=['GET'],responses={200:OutcomeSerializer(many=True)})
@api_view(['GET'])
def control_outcome_view(request):
    if request.user.role == 1:
        outcome_obj = Outcome.objects.all()
        return Response(data=OutcomeSerializer(outcome_obj,many=True).data, status=status.HTTP_200_OK)
    return Response(data={"Error":"Only super user"}, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['POST'], responses={200: UserSerializer(many=True)})
@api_view(['POST'])
def user_register(request):
    if not request.user.is_authenticated:
        return Response({"Error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.role not in [1, 2]:
        return Response({"Error": "Only SuperUser or HR can create new user"}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({"success": f"User {user.username} successfully created!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
