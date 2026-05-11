from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import *
from .serializers import *

# Create your views here.

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Failed to register user.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User logged in successfully.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Failed to log in user.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)   


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)
    



class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data

        if user.is_customer:
            try:
                profile = CustomerProfileSerializer(user.customer_profile).data
            except CustomerProfile.DoesNotExist:
                profile = None
            data['customer_profile'] = profile

        elif user.is_owner:
            try:
                profile = OwnerProfileSerializer(user.owner_profile).data
            except OwnerProfile.DoesNotExist:
                profile = None
            data['owner_profile'] = profile
        return Response(data, status=status.HTTP_200_OK)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get_object(self):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return Response({'message': 'Only customers can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_customer:
            return Response({'message': 'Only customers can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class OwnerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OwnerProfileSerializer

    def get_object(self):
        profile, _ = OwnerProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_owner:
            return Response({'message': 'Only owners can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_owner:
            return Response({'message': 'Only owners can access this endpoint.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'message': 'Password is incorrect.'} , status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            Token.objects.filter(user=user).delete()
            return Response({'message': 'Password changed successfully. Please log in again.'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Failed to change password.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
