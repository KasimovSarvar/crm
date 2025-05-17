from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from  rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer, SimpleLoginSerializer
from django.contrib.auth.hashers import make_password


@swagger_auto_schema(
    method='post',
    operation_summary="HR yoki SuperUser user yaratishi",
    request_body=UserSerializer,
    responses={
        201: openapi.Response(description="User qoshildi", schema=UserSerializer),
        400: "Invalid credentials",
        403: "Permission denied"
    },
    tags=["User"]
)
@api_view(['POST'])
def create_user_view(request):
    creator_role = request.user.role
    new_user_role = int(request.data.get("role", 4))
    if creator_role == 2 and new_user_role == 1:
        return Response({"error": "HR cannot create a SuperUser."}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'errors': "user with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    password = serializer.validated_data["password"]
    user = serializer.save(password=make_password(password))
    # return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response({"message": f"User {user.username} created successfully."}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='post',
    tags=["User"],
    request_body=SimpleLoginSerializer,
    responses={200: "Login successful", 400: "Invalid credentials"}
)
@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

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

  


