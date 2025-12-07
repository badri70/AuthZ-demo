from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.contrib.auth import authenticate
from core.utils import generate_jwt
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsAdmin, IsModerator


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            full_name = serializer.validated_data['full_name']
            email = serializer.validated_data['email']
            password_1 = serializer.validated_data['password_1']
            password_2 = serializer.validated_data['password_2']

            if password_1 != password_2:
                return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=email, email=email, password=password_1, first_name=full_name)
            user.save()

            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                token = generate_jwt(user.pk)
                return Response({"token": token}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        full_name = serializer.validated_data.get("full_name")
        email = serializer.validated_data.get("email")

        if full_name:
            user.first_name = full_name
        if email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response(
                    {"error": "Email already in use"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.email = email
            user.username = email

        user.save()

        return Response({"message": "Profile updated successfully"})
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        user = request.user

        if not user.check_password(old_password):
            return Response(
                {"error": "Старый пароль неверный"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({"message": "Пароль успешно изменен"})


class ProfileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    

class UsersListView(APIView):
    permission_classes = [IsModerator, IsModerator]

    def get(self, request):
        data = [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Anna"},
        {"id": 3, "name": "Mary"},
    ]
        return Response(data)