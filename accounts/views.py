from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpRequest, request
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import routers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

from . import models
from . import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


class UserGetView(APIView):
    def get(self, request):
        objects = models.UserS.objects.all()
        serializer = serializers.GetUserSeriliazer(objects, many=True)
        return Response(serializer.data)


class UserPostView(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegisterSeriliazer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPatchView(APIView):
    def patch(self, request, pk):
        image = models.ProductImages.objects.get(id=pk)
        serializer = serializers.ImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CustomUserToken(TokenObtainPairView):
    pass


class ExampleView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data['refresh']
        return Response({'refresh': refresh_token})

class CustomTokenObtainView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            refresh = RefreshToken.for_user(user_data)
            return Response({"refresh": str(refresh)})
        else:
            return Response("pizdec")


class UserLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            try:
                refresh_token = models.UserRefreshToken.objects.get(user=user)
            except models.UserRefreshToken.DoesNotExist:
                pass
            refresh = RefreshToken.for_user(user)

            models.UserRefreshToken.objects.create(user=user, token=str(refresh))

            access_token = str(refresh.access_token)
            access_refresh = str(refresh)

            response = Response({
                "access_token": access_token,
                "access_refresh": access_refresh,
            }, status=status.HTTP_200_OK)

            response.set_cookie("access_token", access_token, secure=True, httponly=True, samesite="Strict")
            return response
        else:
            return Response("Fail", status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def post(self, request):
        user = request.user

        #delete refresh token
        models.UserRefreshToken.objects.filter(user=user).delete()

        #delete access token

        response = Response({"message": "User logouted"}, status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response














