from .models import *
from .serializers import *
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class  = ActivitySerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            token = get_token_for_user(user)
            return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {"non_field_errors": ['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)        


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Only allow POST requests

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            else:
                # Blacklist all outstanding tokens for the user if no refresh token is provided
                tokens = OutstandingToken.objects.filter(user=request.user)
                for token in tokens:
                    RefreshToken(token.token).blacklist()

            return Response({"msg": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
