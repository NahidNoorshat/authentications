from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisteationSerializer, UserLogingSerializer, UserProfileSerializer, UserChangePasswordSerializer
from django.contrib.auth import authenticate
from .renderers import UserRendere
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationsView(APIView):
    renderer_classes = [UserRendere]
    def post(self, request, format=None):
        serializer = UserRegisteationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Registrations Success !!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    renderer_classes = [UserRendere]
    def post(self, request, format=None):
        serializer = UserLogingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg': 'Login Success !!'}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': {'non_fields_errors': 'Email and Password doesnot match'}}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes=[ IsAuthenticated ]
    renderer_classes = [UserRendere]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePassword(APIView):
    permission_classes= [IsAuthenticated]
    renderer_classes = [UserRendere]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user} )

        if serializer.is_valid(raise_exception=True):
            return Response ({'msg': 'Password Change Sucessfully !!'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)