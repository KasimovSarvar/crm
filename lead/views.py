from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authe.models import User
from authe.serializers import UserSerializer
from .serializers import OutcomeSerializer, LeadSerializer, StudentSerializer
from .models import Outcome, Lead, Student


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

#
@api_view(['POST'])
def create_lead_view(request):
    if request.user.role not in [1, 2]:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    serializer = LeadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    lead = serializer.save(created_by=request.user)
    return Response({"lead": LeadSerializer(lead).data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_user_view(request):
    if request.user.role not in [1, 2]:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    role = request.data["role"]
    if str(role) == "1" or str(role).lower() == "superuser":
        return Response({"error": "SuperUser yaratomis"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    password = serializer.validated_data["password"]
    user = serializer.save(password=make_password(password))
    return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_student_view(request):
    if request.user.role not in [1, 2]:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    serializer = StudentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    student = serializer.save(created_by=request.user)
    return Response({"student": UserSerializer(student).data}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def change_lead_admin_view(request, lead_id):
    if request.user.role not in [1, 2]:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    new_admin_id = request.data["admin_id"]
    if not new_admin_id:
        return Response({'message': 'admin_id yuborilish shart'}, status=status.HTTP_400_BAD_REQUEST)

    new_admin = User.objects.filter(id=new_admin_id, role=4).first()
    if not new_admin:
        return Response({'message': 'Bunday admin mavjud emas'}, status=404)

    lead.admin = new_admin
    lead.save()
    return Response({'message': 'Lead admin yangilandi'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def change_student_admin_view(request, student_id):
    if request.user.role not in [1, 2]:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    student = Student.objects.filter(id=student_id).first()
    if not student:
        return Response({'message': 'Lead topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    new_admin_id = request.data["admin_id"]
    if not new_admin_id:
        return Response({'message': 'admin_id yuborilish shart'}, status=status.HTTP_400_BAD_REQUEST)

    new_admin = User.objects.filter(id=new_admin_id, role=4).first()
    if not new_admin:
        return Response({'message': 'Bunday admin mavjud emas'}, status=404)

    student.admin = new_admin
    student.save()
    return Response({'message': 'Student admin yangilandi'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def lead_list_view(request):
    if request.user.role not in [1, 2]:
        return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    leads = Lead.objects.filter(created_by=request.user)
    serializer = LeadSerializer(leads, many=True)

    return Response({'data': serializer.data}, status=status.HTTP_200_OK)