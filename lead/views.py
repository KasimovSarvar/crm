from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Lead, Comment, State, University, Season, Faculty, Student
from .serializer import LeadSerializer, StudentSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response  
from rest_framework import status
from rest_framework.response import Response
from .serializers import OutcomeSerializer
from .models import Outcome

@api_view(['GET'])
def lead_list_view(request):
    lead = Lead.objects.all()
    serializer = LeadSerializer(lead, many=True)
    return Response({'message':'success'},serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def my_lead_list_view(request):
    user = request.user
    if user.is_authenticate and user.role == 4:
        lead = Lead.objects.filter(admin=user)
        serializer = LeadSerializer(lead, many=True)
        return Response({'message':'success'},serializer.data)
    return HttpResponse({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PUT'])
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

 

@api_view(['POST'])
def create_student_view(request, lead_id):
    data = request.data
    user = request.user
    
    lead = Lead.objects.get(id=data['lead'])
    
    if not user.is_authenticated and user.role == 4:
        return HttpResponse({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        return Response({'detail': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not lead.admin == user:
        return HttpResponse({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message':'error in creating student'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def my_students_list_view(request):
    user = request.user
    if user.is_authenticate and user.role == 4:
        student = Student.objects.filter(admin=user)
        serializer = StudentSerializer(student, many=True)
        return Response({'message':'success'},serializer.data)
    return HttpResponse({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PATCH'])
def student_update_view(request, pk):
    data = request.data
    user = request.user
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.is_authenticated and user.role == 4:
        return HttpResponse({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)
    
    if not student.admin == user:
        return HttpResponse({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = StudentSerializer(student, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'success! update this student'},serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def outcome_view(request):
    if request.user.role != 3:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        outcomes = Outcome.objects.all()
        serializer = OutcomeSerializer(outcomes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = OutcomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)