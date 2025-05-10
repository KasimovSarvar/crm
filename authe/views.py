from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view , permission_classes
from .serializers import  UserSerializer

@swagger_auto_schema(method='post', request_body=UserSerializer)
@permission_classes(['IsAuthenticated'])
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

