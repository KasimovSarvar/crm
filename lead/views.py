from datetime import datetime, date
from calendar import monthrange
from django.utils.timezone import now
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authe.models import User
from authe.serializers import UserSerializer
from .serializers import LeadSerializer, StudentSerializer, PaymentSerializer, LeadCreateSerializer, PaymentCreateSerializer, CommentSerializer
from .serializers import StudentSerializer, PaymentSerializer, LeadSerializer, PaymentCreateSerializer
from .models import Outcome, Lead, Student, Payment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    responses={200: PaymentSerializer(many=True)},
    tags=["Payment"]
)
@api_view(['GET'])
def payment_list_admin(request):
    if request.user.role == 4:
        payment = Payment.objects.filter(student__admin=request.user)
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)
    return Response({'error': 'You are not allowed to payments'})

@swagger_auto_schema(
    method='get',
    responses={200: PaymentSerializer(many=True)},
    tags=["Payment"]
)
@api_view(['GET'])
def payment_list_hr(request):
    if request.user.role in [1, 2]:
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)
    return Response({'error': 'You are not allowed to payments'})


@swagger_auto_schema(
    method='post',
    request_body=PaymentCreateSerializer,
    responses={201: PaymentCreateSerializer},
    tags=["Payment"]
)
@api_view(['POST'])
def create_payment(request):
    serializer = PaymentCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(check_uploader=request.user)
        return Response({"message": "payment created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PATCH',
    request_body=PaymentSerializer,
    responses={
        200: PaymentSerializer,
        404: openapi.Response(description="Payment not found")
    },
    tags=["Payment"]
)
@api_view(['PATCH'])
def update_payment(request, pk):
    payment = Payment.objects.filter(id=pk).first()
    if not payment:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PaymentSerializer(payment, data=request.data)
    if serializer.is_valid():
        serializer.save(confirmatory=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PATCH',
    request_body=PaymentCreateSerializer,
    responses={
        200: PaymentCreateSerializer,
        400: "Invalid credentials"
    },
    tags=["Payment"]
)
@api_view(['PATCH'])
def update_payment_admin(request, student_id, payment_id):
    payment = Payment.objects.filter(student__id=student_id, id=payment_id, student__admin=request.user).first()
    print(payment)

    if not payment:
        return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

    if payment.confirmatory is not None or payment.is_payed == "payed":
        return Response(
            {"detail": "You cannot update a confirmed or fully paid payment."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = PaymentCreateSerializer(payment, data=request.data, partial=True)
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
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    if not start or not end:
        today = now().date()
        year, month = today.year, today.month
        start_date = date(year, month, 1)
        end_day = monthrange(year, month)[1]
        end_date = date(year, month, end_day)
    else:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()

    incomes = Payment.objects.filter(
        is_payed='payed',
        created_at__date__range=(start_date, end_date)
    )
    expenses = Outcome.objects.filter(
        created_at__date__range=(start_date, end_date)
    )

    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return Response({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense
    }, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def balance_report(request):
#     total_income = Payment.objects.filter(is_payed='payed').aggregate(Sum('amount'))['amount__sum']
#     total_expense = Outcome.objects.aggregate(Sum('amount'))['amount__sum']
#     balance = total_income - total_expense
#
#     return Response({
#         'total_income': total_income,
#         'total_expense': total_expense,
#         'balance': balance
#     }, status=status.HTTP_200_OK)


# HR
@swagger_auto_schema(
    method='post',
    operation_summary="HR yoki SuperUser lead yaratishi",
    request_body=LeadCreateSerializer,
    responses={
        201: openapi.Response(description="Lead qoshildi", schema=LeadCreateSerializer),
        400: "Invalid credentials"
    },
    tags=["Lead"]
)
@api_view(['POST'])
def create_lead_view_hr(request):
    serializer = LeadCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save(created_by=request.user, admin=None)
    return Response({"message": "lead created successfully"}, status=status.HTTP_201_CREATED)



@swagger_auto_schema(
    method='post',
    operation_summary="Admin lead yaratishi",
    request_body=LeadCreateSerializer,
    responses={
        201: openapi.Response(description="Lead qoshildi", schema=LeadCreateSerializer),
        400: "Invalid credentials"
    },
    tags=["Lead"]
)
@api_view(['POST'])
def create_lead_view_admin(request):
    serializer = LeadCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save(created_by=request.user, admin=request.user)
    return Response({"message": "lead created successfully"}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    operation_summary="HR yoki SuperUser student yaratishi",
    request_body=StudentSerializer,
    responses={
        201: openapi.Response(description="Student qoshildi", schema=StudentSerializer),
        400: "Invalid credentials",
        403: "Permission denied",
        404: "Lead not found"
    },
    tags=["Student"]
)
@api_view(['POST'])
def create_student_view_hr(request, lead_id):
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    data["first_name"] = lead.first_name
    data["last_name"] = lead.last_name
    data["phone_number"] = lead.phone_number
    data['passport_series'] = lead.passport_series
    
    serializer = StudentSerializer(data=data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    student = serializer.save(created_by=request.user, admin=None)
    lead.status = 'closed'
    lead.save()
    return Response({"message": f"{student} created successfully"}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='post',
    operation_summary="Admin student yaratishi",
    request_body=StudentSerializer,
    responses={
        201: openapi.Response(description="Student qoshildi", schema=StudentSerializer),
        400: "Invalid credentials",
        403: "Permission denied",
        404: "Lead not found"
    },
    tags=["Student"]
)
@api_view(['POST'])
def create_student_view_admin(request, lead_id):
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)

    if lead.admin != request.user:
        return Response({'message': 'This lead is not assigned to you'}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.copy()
    data["first_name"] = lead.first_name
    data["last_name"] = lead.last_name
    data["phone_number"] = lead.phone_number
    data['passport_series'] = lead.passport_series

    serializer = StudentSerializer(data=data)
    if not serializer.is_valid():
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
    student = serializer.save(created_by=request.user, admin=request.user)
    lead.status = 'closed'
    lead.save()
    return Response({"message": f"{student} created successfully"}, status=status.HTTP_201_CREATED)


# @swagger_auto_schema(
#     method='put',
#     operation_summary="HR yoki SuperUser leadni adminini ozgartirishi",
#     request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
#         'admin_id': openapi.Schema(type=openapi.TYPE_INTEGER)
#     }),
#     responses={
#         200: "Leadi admini ozgratirildi",
#         400: "admin_id yoki notogri",
#         403: "Permission denied",
#         404: "Lead yoki admin topilmadi"
#     },
#     tags=["Lead"]
# )
# @api_view(['PUT'])
# def change_lead_admin_view(request, lead_id):
#     lead = Lead.objects.filter(id=lead_id).first()
#     if not lead:
#         return Response({'message': 'Lead topilmadi'}, status=status.HTTP_404_NOT_FOUND)
#
#     new_admin_id = request.data["admin_id"]
#     if not new_admin_id:
#         return Response({'message': 'admin_id yuborilish shart'}, status=status.HTTP_400_BAD_REQUEST)
#
#     new_admin = User.objects.filter(id=new_admin_id, role=4).first()
#     if not new_admin:
#         return Response({'message': 'Bunday admin mavjud emas'}, status=status.HTTP_404_NOT_FOUND)
#
#     lead.admin = new_admin
#     lead.save()
#     return Response({'message': 'Lead admin yangilandi'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='put',
    operation_summary="HR yoki SuperUser leadlarni adminini ozgartirishi",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_admin_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            "leads": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
        }
    ),
    responses={
        200: "Leadlar yengi adminga ozgartirildi",
        400: "New_admin_id majburiy yoki noto'g'ri leads",
        404: "New_admin_id boyicha admin yoki leadlar topilmadi"
    },
    tags=["Lead"]
)
@api_view(['PUT'])
def change_leads_admin_view(request):
    lead_ids = request.data.get("leads")
    new_admin_id = request.data.get("new_admin_id")

    if not new_admin_id:
        return Response({'message': 'New_admin_id majburiy'}, status=status.HTTP_400_BAD_REQUEST)

    new_admin = User.objects.filter(id=new_admin_id, role=4).first()
    if not new_admin:
        return Response({'message': 'New_admin_id boyicha admin topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    leads = Lead.objects.filter(id__in=lead_ids)
    if not leads.exists():
        return Response({'message': 'Berilgan idlar boyicha leadlar yoq'}, status=status.HTTP_404_NOT_FOUND)

    leads.update(admin=new_admin)

    return Response({'message': 'Leadlar yengi adminga ozgartirildi'}, status=status.HTTP_200_OK)




# @swagger_auto_schema(
#     method='put',
#     operation_summary="HR yoki SuperAdmin student admin ozgartirishi",
#     request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
#         'admin_id': openapi.Schema(type=openapi.TYPE_INTEGER)
#     }),
#     responses={
#         200: "Student admin ozgraildi",
#         400: "admin_id shart yoki notogri",
#         403: "Permission denied",
#         404: "Student yoki admin topilmadi"
#     },
#     tags=["Student"]
# )
# @api_view(['PUT'])
# def change_student_admin_view(request, student_id):
#     student = Student.objects.filter(id=student_id).first()
#     if not student:
#         return Response({'message': 'Lead topilmadi'}, status=status.HTTP_404_NOT_FOUND)
#
#     new_admin_id = request.data["admin_id"]
#     if not new_admin_id:
#         return Response({'message': 'admin_id yuborilish shart'}, status=status.HTTP_400_BAD_REQUEST)
#
#     new_admin = User.objects.filter(id=new_admin_id, role=4).first()
#     if not new_admin:
#         return Response({'message': 'Bunday admin mavjud emas'}, status=404)
#
#     student.admin = new_admin
#     student.save()
#     return Response({'message': 'Student admin yangilandi'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='put',
    operation_summary="HR yoki SuperUser studentlarni adminini ozgartirishi",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_admin_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            "students": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
        }
    ),
    responses={
        200: "Studentlar yengi adminga ozgartirildi",
        400: "New_admin_id majburiy yoki",
        404: "New_admin_id boyicha admin yoki studentlar topilmadi"
    },
    tags=["Student"]
)
@api_view(['PUT'])
def change_students_admin_view(request):
    students = request.data.get("students")
    new_admin_id = request.data.get("new_admin_id")

    if not new_admin_id:
        return Response({'message': 'New_admin_id majburiy'}, status=status.HTTP_400_BAD_REQUEST)

    new_admin = User.objects.filter(id=new_admin_id, role=4).first()
    if not new_admin:
        return Response({'message': 'New_admin_id boyicha admin topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    all_students = Student.objects.filter(id__in=students)
    if not all_students.exists():
        return Response({'message': 'Berilgan idlar boyicha studentlar yoq'}, status=status.HTTP_404_NOT_FOUND)

    all_students.update(admin=new_admin)
    return Response({'message': 'Studentlar yengi adminga ozgartirildi'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="Admin ozi yaratgan leadlarini korishi",
    responses={
        200: openapi.Response(description="Leadlari", schema=LeadSerializer(many=True)),
        403: "Permission denied"
    },
    tags=["Lead"]
)
@api_view(['GET'])
def lead_list_view_admin(request):
    leads = Lead.objects.filter(admin=request.user)
    serializer = LeadSerializer(leads, many=True)
    return Response({'your_leads': serializer.data}, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='get',
    operation_summary="Hr hamma eadlani korishi",
    responses={
        200: openapi.Response(description="Leadlar", schema=LeadSerializer(many=True)),
        403: "Permission denied"
    },
    tags=["Lead"]
)
@api_view(['GET'])
def lead_list_view_hr(request):
    leads = Lead.objects.all()
    serializer = LeadSerializer(leads, many=True)
    return Response({'leads': serializer.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_summary="Admin ozi yaratgan studentlarini korishi",
    responses={
        200: openapi.Response(description="Studentlari", schema=StudentSerializer(many=True)),
        403: "Permission denied"
    },
    tags=["Student"]
)
@api_view(['GET'])
def student_list_view_admin(request):
    students = Student.objects.filter(admin=request.user)
    serializer = StudentSerializer(students, many=True)
    return Response({'your students': serializer.data}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_summary="Hr hamma studentlarni korishi",
    responses={
        200: openapi.Response(description="Studentlar", schema=StudentSerializer(many=True)),
        403: "Permission denied"
    },
    tags=["Student"]
)
@api_view(['GET'])
def student_list_view_hr(request):
    student = Student.objects.all()
    serializer = StudentSerializer(student, many=True)
    return Response({'students': serializer.data}, status=status.HTTP_200_OK)
# END HR...


@swagger_auto_schema(
    method='put',
    operation_summary="Lead ma'lumotlarini yangilash",
    # manual_parameters=[
    #     openapi.Parameter('lead_id', openapi.IN_PATH, description="Lead ID", type=openapi.TYPE_INTEGER)
    # ],
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
def lead_update_view(request, pk):
    lead = Lead.objects.filter(id=pk).first()
    
    if not lead:
        return Response({'message': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)
   
    is_student = Student.objects.filter(passport_series=lead.passport_series).exists()

    if request.user.role == 4:
        if lead.status == 'canceled':
            return Response({'message': 'You con not update ->  Canceled lead..!' }, status=status.HTTP_400_BAD_REQUEST)
        if is_student:
            return Response({'message': 'if this lead already has student -> you can not update'}, status=status.HTTP_400_BAD_REQUEST)
  
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success!!! update this lead', 'data': serializer.data}, status=status.HTTP_200_OK)
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
def create_student(request, lead_id):
   
    lead = Lead.objects.filter(id=lead_id).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=404)

    if request.user.role == 4 and lead.admin != request.user:
        return Response({'message': 'this lead not for you'}, status=403)

    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user, admin=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


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
def student_detail(request, pk):
    student = Student.objects.filter(id=pk).first()
    if not student:
        return Response({'message': 'Student not found'}, status=404)

    if request.user.role == 4 and student.admin != request.user:
        return Response({'message': 'this student not for you'}, status=403)

    serializer = StudentSerializer(student)
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_summary="Leadga comment qoshish",
    request_body=CommentSerializer,
    responses={
        200: openapi.Response("Comment qo'shildi", CommentSerializer),
        400: "Not authenticated or validation error",
        403: "Access denied",
        404: "Lead not found"
    },
    tags=["Lead"]
)

@api_view(['POST'])
def add_comment_view(request, pk):
    lead = Lead.objects.filter(id=pk).first()
    if not lead:
        return Response({'message': 'Lead not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role != 4:
        return Response({'message': 'this lead not for you'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(admin=request.user, lead=lead)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)