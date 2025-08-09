from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class RegisterApi(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': 'serializer.data', 'status':status.HTTP_200_OK})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
