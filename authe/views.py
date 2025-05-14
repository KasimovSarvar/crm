from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from  rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer



@swagger_auto_schema(methods=['POST'],responses={200:UserSerializer(many=True)})
@api_view(http_method_names=['POST'])
def register_view(request):
    # if not request.user.is_authenticated:
    #     return Response({"Error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user.role not in [1,2]:
        return Response(data={"Error": "Only SuperUser and HR can create new user"},status=status.HTTP_400_BAD_REQUEST)

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
    access_token = refresh_token.access_token

    return Response(data={"access_token":str(access_token),"refresh_token":str(refresh_token)},status=status.HTTP_200_OK)

  


