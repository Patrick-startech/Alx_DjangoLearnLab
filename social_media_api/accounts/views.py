# Create your views here.
# accounts/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(APIView):
    """
    Handle user registration.
    Creates a new user, generates an auth token, and returns user data.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user, context={'request': request}).data
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    Handle user login.
    Validates credentials, returns existing or new auth token, and user data.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user, context={'request': request}).data
            },
            status=status.HTTP_200_OK
        )


class ProfileView(RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowUserView(APIView):
    """
    Allow an authenticated user to follow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response(
                {'detail': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.add(target)
        return Response(
            {'detail': f'Now following {target.username}.'},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(APIView):
    """
    Allow an authenticated user to unfollow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response(
                {'detail': 'You cannot unfollow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.user.following.remove(target)
        return Response(
            {'detail': f'Unfollowed {target.username}.'},
            status=status.HTTP_200_OK
        )
