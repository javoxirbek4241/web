from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class RegisterApi(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': 'serializer.data', 'status':status.HTTP_200_OK})
        return Response({'message': serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})

class LoginApi(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Username yoki parol xato!"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Chiqildi"}, status=status.HTTP_200_OK)
