from .models import *
from .serializers import *
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import F, Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
import django_filters.rest_framework as filters
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.decorators import action

UserAccount = get_user_model()


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

  


class ActivityFilter(filters.FilterSet):
    project = filters.ModelMultipleChoiceFilter(
        field_name='project',
        queryset=Project.objects.filter(),  # Set default empty queryset
        label='Project Names'
    )

    class Meta:
        model = Activity
        fields = ['project']


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ActivityFilter

    def get_queryset(self):
        # user=self.request.user
        qs = Activity.objects.filter()
        # .annotate(project_name=F("project__name"))
        return qs

    def perform_create(self, serializer):
        if isinstance(serializer.validated_data, list):
            # Bulk create if serializer data is a list
            activities = [Activity(user=self.request.user, **item) for item in serializer.validated_data]
            Activity.objects.bulk_create(activities)
        else:
            # Single object creation
            serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            # If request data is a list, many=True for bulk create
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            # Otherwise, treat as a single object
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


    # custom action list current user invitation

class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer


# class RegisterView(generics.CreateAPIView):
#     queryset = UserAccount.objects.all()
#     serializer_class = UserAccountSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         data = serializer.data
#         return Response(data, status=status.HTTP_201_CREATED)

# def get_token_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

# class UserLoginView(generics.CreateAPIView):
#     serializer_class = UserLoginSerializer
#     queryset = UserAccount.objects.all()
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data.get('email')
#         password = serializer.validated_data.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             token = get_token_for_user(user)
#             return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'errors': {"non_field_errors": ['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)        


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['post']  # Only allow POST requests

#     def post(self, request, *args, **kwargs):
#         try:
#             refresh_token = request.data.get("refresh")
#             if refresh_token:
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()
#             else:
#                 # Blacklist all outstanding tokens for the user if no refresh token is provided
#                 tokens = OutstandingToken.objects.filter(user=request.user)
#                 for token in tokens:
#                     RefreshToken(token.token).blacklist()

#             return Response({"msg": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
