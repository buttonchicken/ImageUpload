from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

# Create your views here.

class Register(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        mobile_number = request.data['mobile_number']
        seller = request.query_params['seller']
        if len(user.objects.filter(username=username))!=0:
            return Response({'success': False, "message": "Username already exists!!"},status=status.HTTP_400_BAD_REQUEST)
        user_object = user()
        user_object.username=username
        user_object.set_password(password)
        user_object.mobile_number=mobile_number
        user_object.IsSeller=seller
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object.save()        
        # user_obj = user.objects.get(username=username)
        refresh = RefreshToken.for_user(user_object)
        return Response({"success": True, "message": "Your account has been successfully activated!!",
                'payload': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)},
                status=status.HTTP_202_ACCEPTED)

class Login(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = RegisterSerializer(user)
            return Response({"success": True, "message": "Login successful",
                            'payload': serializer.data,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)