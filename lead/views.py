from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authe.models import User
from authe.serializers import UserSerializer
from .serializers import LeadSerializer, StudentSerializer, PaymentSerializer,PaymentCreateSerializer
from .models import Outcome, Lead, Student, Payment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['PUT'])
def update_payment_admin(request, pk):
    payment = Payment.objects.filter(pk=pk, student__admin=request.user).first()
    if not payment:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

    if payment.confirmatory is not None or payment.is_payed == "payed":
        return Response({"detail": "You cannot update a confirmed or fully paid payment."},status=status.HTTP_400_BAD_REQUEST)

    serializer = PaymentCreateSerializer(payment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@swagger_auto_schema(
    method='get',
    responses={200: PaymentSerializer(many=True)},
    tags=["Payment"]
)
@api_view(['GET'])
def payment_list(request):
    payments = Payment.objects.all()
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=PaymentSerializer,
    responses={201: PaymentSerializer},
    tags=["Payment"]
)
@api_view(['POST'])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    request_body=PaymentSerializer,
    responses={
        200: PaymentSerializer,
        404: openapi.Response(description="Payment not found")
    },
    tags=["Payment"]
)
@api_view(['PUT'])
def update_payment(request, pk):
    payment = Payment.objects.filter(id=pk).first()
    if not payment:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(description="Returns total income, expense, and balance.")
    },
    tags=["Payment"]
)
@api_view(['GET'])
def balance_report(request):
    total_income = Payment.objects.filter(is_payed='payed').aggregate(Sum('amount'))['amount__sum']
    total_expense = Outcome.objects.aggregate(Sum('amount'))['amount__sum']
    balance = total_income - total_expense

    return Response({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance
    }, status=status.HTTP_200_OK)


# HR
@swagger_auto_schema(
    method='post',
    operation_summary="HR yoki SuperUser lead yaratishi",
    request_body=LeadSerializer,
    responses={
        201: openapi.Response(description="Lead qoshildi", schema=LeadSerializer),
        400: "Invalid credentials",
        403: "Permission denied"
    },
    tags=["Lead"]
)
@api_view(['POST'])
@api_view(['POST'])
def create_lead_view(request):
    serializer = LeadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    lead = serializer.save(created_by=request.user)
    return Response({"lead": LeadSerializer(lead).data}, status=status.HTTP_201_CREATED)


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
    role = request.data["role"]
    if str(role) == "1" or str(role).lower() == "superuser":
        return Response({"error": "SuperUser yaratomis"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    password = serializer.validated_data["password"]
    user = serializer.save(password=make_password(password))
    return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    operation_summary="HR yoki SuperUser student yaratishi",
    request_body=StudentSerializer,
    responses={
        201: openapi.Response(description="Student qoshildi", schema=StudentSerializer),
        400: "Invalid credentials",
        403: "Permission denied"
    },
    tags=["Student"]
)
@api_view(['POST'])
def create_student_view(request):
    serializer = StudentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    student = serializer.save(created_by=request.user)
    return Response({"student": UserSerializer(student).data}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='put',
    operation_summary="HR yoki SuperUser leadni adminini ozgartirishi",
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'admin_id': openapi.Schema(type=openapi.TYPE_INTEGER)
    }),
    responses={
        200: "Leadi admini ozgratirildi",
        400: "admin_id yoki notogri",
        403: "Permission denied",
        404: "Lead yoki admin topilmadi"
    },
    tags=["Lead"]
)
@api_view(['PUT'])
def change_lead_admin_view(request, lead_id):
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    new_admin_id = request.data["admin_id"]
    if not new_admin_id:
        return Response({'message': 'admin_id yuborilish shart'}, status=status.HTTP_400_BAD_REQUEST)

    new_admin = User.objects.filter(id=new_admin_id, role=4).first()
    if not new_admin:
        return Response({'message': 'Bunday admin mavjud emas'}, status=status.HTTP_404_NOT_FOUND)

    lead.admin = new_admin
    lead.save()
    return Response({'message': 'Lead admin yangilandi'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='put',
    operation_summary="HR yoki SuperAdmin student admin ozgartirishi",
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'admin_id': openapi.Schema(type=openapi.TYPE_INTEGER)
    }),
    responses={
        200: "Student admin ozgraildi",
        400: "admin_id shart yoki notogri",
        403: "Permission denied",
        404: "Student yoki admin topilmadi"
    },
    tags=["Student"]
)
@api_view(['PUT'])
def change_student_admin_view(request, student_id):
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


@swagger_auto_schema(
    method='get',
    operation_summary="HR ozi yaratgan leadlarini korishi",
    responses={
        200: openapi.Response(description="Leadlari", schema=LeadSerializer(many=True)),
        403: "Permission denied"
    },
    tags=["Lead"]
)
@api_view(['GET'])
def lead_list_view(request):
    if request.user_role == 2:
        leads = Lead.objects.filter(created_by=request.user_role)
        serializer = LeadSerializer(leads, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="HR ozi yaratgan studentlarini korishi",
    responses={
        200: openapi.Response(description="Studentlari", schema=StudentSerializer(many=True)),
        403: "Permission denied"
    },
    tags=["Student"]
)
@api_view(['GET'])
def student_list_view(request):
    if request.user_role == 2:
        students = Student.objects.filter(admin=request.user_role)
        serializer = StudentSerializer(students, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    student = Student.objects.all()
    serializer = StudentSerializer(student, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)


# END HR...
@swagger_auto_schema(
    method='get',
    operation_summary="Admin uchun Leadlar ro'yxati",
    responses={
        200: openapi.Response("Leadlar ro'yxati", LeadSerializer(many=True)),
        400: "Not authenticated"
    },
    tags=["Lead"]
)
@api_view(['GET'])
def admin_lead_view(request):
    if request.user.role == 4:
        leads = Lead.objects.filter(admin=request.user)
    else:
        leads = Lead.objects.all()

    serializer = LeadSerializer(leads, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='put',
    operation_summary="Lead ma'lumotlarini yangilash",
    manual_parameters=[
        openapi.Parameter('lead_id', openapi.IN_PATH, description="Lead ID", type=openapi.TYPE_INTEGER)
    ],
    request_body=LeadSerializer,
    responses={
        200: openapi.Response("Yangilangan lead ma'lumotlari", LeadSerializer()),
        400: "Not authenticated or validation error",
        403: "Access denied",
        404: "Lead not found"
    },
    tags=["Lead"]
)
@api_view(['PUT'])
def lead_update_view(request, lead_id):
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role == 4:
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success! update this lead'}, serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(
    method='post',
    operation_summary="Yangi student yaratish",
    request_body=StudentSerializer,
    responses={
        201: openapi.Response("Yaratilgan student ma'lumotlari", StudentSerializer()),
        400: "Not authenticated or validation error",
        403: "Access denied",
        404: "Lead not found"
    },
    tags=["Student"]
)
@api_view(['POST'])
def create_student(request):
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


@swagger_auto_schema(
    method='get',
    operation_summary="Adminning studentlar ro'yxati",
    responses={
        200: openapi.Response("Studentlar ro'yxati", StudentSerializer(many=True)),
        400: "Not authenticated",
        403: "Access denied"
    },
    tags=["Student"]
)
@api_view(['GET'])
def my_students_list_view(request):
    if request.user.role == 4:
        student = Student.objects.filter(admin=request.user)
        serializer = StudentSerializer(student, many=True)
        return Response({'message': 'success'}, serializer.data)
    return Response({'message': 'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(
    method='patch',
    operation_summary="Student ma'lumotlarini yangilash",
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="Student ID", type=openapi.TYPE_INTEGER)
    ],
    request_body=StudentSerializer,
    responses={
        200: openapi.Response("Yangilangan student ma'lumotlari", StudentSerializer()),
        400: "Not authenticated or validation error",
        403: "Access denied",
        404: "Student not found"
    },
    tags=["Student"]
)
@api_view(['PATCH'])
def student_update_view(request, pk):
    data = request.data
    user = request.user

    student = Student.objects.filter(id=pk).first()
    if not student:
        return Response({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.role != 4:
        return Response({'message': 'You are not Admin'}, status=status.HTTP_403_FORBIDDEN)

    if not student.admin == user:
        return Response({'message': 'You can not update this student'}, status=status.HTTP_403_FORBIDDEN)

    serializer = StudentSerializer(student, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'success! update this student'}, serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_summary="Studentning batafsil ma'lumotini olish",
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="Student ID", type=openapi.TYPE_INTEGER)
    ],
    responses={
        200: openapi.Response("Student ma'lumotlari", StudentSerializer()),
        400: "Not authenticated",
        403: "Access denied",
        404: "Student not found"
    },
    tags=["Student"]
)
@api_view(['GET'])
def student_detail(request, id):
    student = Student.objects.filter(id=id).first()
    if not student:
        return Response({'message': 'Student not found'}, status=404)

    if request.user.role == 4 and student.lead.admin != request.user:
        return Response({'message': 'this student not for you'}, status=403)

    serializer = StudentSerializer(student)
    return Response(serializer.data)
