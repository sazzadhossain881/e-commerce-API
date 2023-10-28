from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from core import models
from core import serializers

from django.contrib.auth.hashers import make_password
from core.authentication import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    JWTAuthentication,
    decode_refresh_token,
)
import datetime
import random
import string


# Create your views here.
class RegisterApiView(APIView):

    def post(self, request):
        data = request.data
        try:
            user = models.User.objects.create(
                email=data['email'],
                name=data['name'],
                password=make_password(data['password']),
            )
            serializer = serializers.UserSerializer(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'user with this email already exists.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

       

class LoginApiView(APIView):

    def post(self, request):
        
        email = request.data['email']
        password = request.data['password']

        user = models.User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('invalid credentials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        models.UserToken.objects.create(
            user_id=user.id,
            token = refresh_token,
            expire_at = datetime.datetime.utcnow()+datetime.timedelta(days=7)
        )

        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data={
            'token':access_token,
            'email':user.email,
            'name':user.name,
            'isAdmin':user.is_staff
        }
        return response


class UserApiView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        return Response(serializers.UserSerializer(request.user).data)

class RefreshApiView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not models.UserToken.objects.filter(
            user_id=id,
            token = refresh_token,
            expire_at__gt = datetime.datetime.now(tz=datetime.timezone.utc)
        ).exists():
            raise exceptions.AuthenticationFailed('unauthenticated')


        access_token = create_access_token(id)
        return Response({
            'token':access_token
        })

class LogoutApiView(APIView):
    # authentication_classes = [JWTAuthentication]
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        models.UserToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key="refresh_token")
        response.data = {
            'message':'success'
        }
        return response

class UsersApiView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        users = models.User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

class DeleteApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    def delete(self, request, pk):
        user = models.User.objects.get(pk=pk)
        user.delete()
        return Response('user was deleted')

class UpdateApiView(APIView):

    def put(self, request, pk):
        user = models.User.objects.get(pk=pk)

        data = request.data

        user.name = data['name']
        user.email = data['email']
        user.is_staff = data['isAdmin']

        user.save()

        serializer = serializers.UserSerializer(user, many=False)
        return Response(serializer.data)

class RetrieveUserApiView(APIView):

    def get(self, request, pk):
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            return Response({'error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.UserSerializer(user, many=False)
        return Response(serializer.data)
    