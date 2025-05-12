from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Lead, Comment, State, University, Season, Faculty, Student
from .serializer import LeadSerializer, StudentSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import OutcomeSerializer
from .models import Outcome
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status


@api_view(['GET'])
def lead_list(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.role == 4:
        leads = Lead.objects.filter(admin=request.user)
    else:
        leads = Lead.objects.all()
    
    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def lead_update_view(request, lead_id):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user.role == 4:
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'success! update this lead'},serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)
    

 

@api_view(['POST'])
def create_student(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    lead_id = request.data.get("lead")

    if not lead_id:
        return Response({'message': 'Lead id not found'}, status=400)

    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=404)

    if request.user.role == 4 and lead.admin != request.user:
        return Response({'message': 'this lead not for you'}, status=403)

    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def my_students_list_view(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user.role == 4:
        student = Student.objects.filter(admin=request.user)
        serializer = StudentSerializer(student, many=True)
        return Response({'message':'success'},serializer.data)
    return Response({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['PATCH'])
def student_update_view(request, pk):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = request.data
    user = request.user

    student = Student.objects.filter(id=pk).first()
    if not student:
        return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.role != 4:
        return Response({'message':'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)
    
    if not student.admin == user:
        return Response({'message':'You can not update this student'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = StudentSerializer(student, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'success! update this student'},serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def student_detail(request, id):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    student = Student.objects.filter(id=id).first()
    if not student:
        return Response({'message': 'Student not found'}, status=404)

    if request.user.role == 4 and student.lead.admin != request.user:
        return Response({'message': 'this student not for you'}, status=403)

    serializer = StudentSerializer(student)
    return Response(serializer.data)

 