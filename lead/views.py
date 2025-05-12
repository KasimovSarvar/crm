from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import OutcomeSerializer
from .models import Outcome

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