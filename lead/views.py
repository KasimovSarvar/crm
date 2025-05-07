from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Lead, Comment, State, University, Season, Faculty, Student
from .serializer import LeadSerializer, StudentSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response  
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lead_list_view(request):
    user = request.user
    if user.role in ['Admin', 'SuperUser']:
        lead = Lead.objects.filter(admin=user)
        serializer = LeadSerializer(lead, many=True)
        return Response({'message':'success'},serializer.data)
    return HttpResponse({'message':'You are not Admin or Superuser'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def lead_update_view(request, lead_id):
    user = request.user
    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        return Response({'detail': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.role in ['Admin', 'SuperUser'] and lead.admin == user:
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'success! update this lead'},serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'detail': 'You are not authorized to update this lead'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def lead_delete_view(request, pk):
    user = request.user
    try:
        lead = Lead.objects.get(pk=pk, admin=user)  
    except Lead.DoesNotExist:
        return Response({'detail': 'Lead not found or you are not authorized to delete this lead'}, status=status.HTTP_404_NOT_FOUND)
    
    lead.delete()   
    return Response({'detail': 'Lead deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

