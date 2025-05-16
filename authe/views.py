from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from  rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer,SimpleLoginSerializer
from django.contrib.auth.hashers import make_password



@swagger_auto_schema(methods=['POST'],
request_body=UserSerializer,
responses={200:UserSerializer(many=True)},
tags=["User"])
@api_view(http_method_names=['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if serializer.validated_data.get('role') == 1:
        return Response(
            {"error": "Only Admin Panel can create a SuperUser."},
            status=status.HTTP_400_BAD_REQUEST
        )

    validated_data = serializer.validated_data
    raw_password = validated_data.get('password')

    user_obj = User(
        username=validated_data.get('username'),
        role=validated_data.get('role'),
        full_name=validated_data.get("full_name"),
        fixed_salary=validated_data.get("fixed_salary"),
        phone_number=validated_data.get("phone_number"),
        status=validated_data.get("status"),
        lead_number=validated_data.get("lead_number"),
        login_time=validated_data.get("login_time"),
        password=make_password(raw_password)
    )
    user_obj.save()

    return Response({"message": f"User {user_obj.username} created successfully."}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='post',
    tags=["User"],
    request_body=SimpleLoginSerializer,
    responses={200: "Login successful", 400: "Invalid credentials"}
)
@api_view(['POST'])
def login_view(request):
    username = request.data["username"]
    password = request.data["password"]

    if not username or not password:
        return Response({"message": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user_model = User.objects.filter(username=username).first()
    print(user_model)
    if not user_model:
        return Response(data={"Error":"Username not found"},status=status.HTTP_400_BAD_REQUEST)

    if not check_password(password,user_model.password):
        return Response(data={"Error":"Wrong password"},status=status.HTTP_400_BAD_REQUEST)


    refresh_token = RefreshToken.for_user(user_model)
    access_token = refresh_token.access_token
    access_token['role'] = user_model.role

    return Response(data={"access_token":str(access_token),"refresh_token":str(refresh_token)},status=status.HTTP_200_OK)

  


