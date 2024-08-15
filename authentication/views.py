from django.shortcuts import render
from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated
# from authentication.serializers import ProfileSerializer, CreateProfileSerializer
from authentication.models import UserAccount #, Profile
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from rest_framework import generics
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from authentication.serializers import UserAccountSerializer #,MeSerializer


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to the homepage or dashboard after signup
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})
    
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
 
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superuser:
                return HttpResponseNotFound("Page not found.")
            login(request, user)
            return redirect('profile')  # Redirect to the profile/dashboard
        else:
            # Handle invalid login attempt
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


@login_required(login_url="/login/")
def dashboard_view(request):
    if request.user.is_superuser:
        return HttpResponseNotFound("Page not found.")
    return render(request, 'dashboard.html', {'user': request.user})


def user_logout(request):
    if request.user.is_superuser:
        return HttpResponseNotFound("Page not found.")
    logout(request)
    return HttpResponseRedirect('/auth/login/')


@login_required(login_url="/login/")
def user_list_view(request):
    if request.user.is_superuser:
        return HttpResponseNotFound("Page not found.")
    users = UserAccount.objects.filter(is_superuser=False)
    return render(request, 'users.html', {'users': users})



@login_required
def update_user(request, pk):
    user = get_object_or_404(UserAccount, pk=pk)
    if request.user.id != user.id:
        return redirect('user_list')  
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated successfully.')
            return redirect('user_list')  # Adjust this based on your view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'signup.html', {'form': form})



@login_required
def delete_user(request, pk):
    user = get_object_or_404(UserAccount, pk=pk)
    
    if request.user.id != user.id:
        return redirect('user_list') 
    
    if request.method == 'POST' and 'confirm' in request.POST:
        user.delete()
        return redirect('login') 
    
    return render(request, 'confirm_delete.html', {'user': user})























#------------------------------------------------------------------drf views----------------------------------------------------------

# class SignupView(generics.CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [AllowAny]


# class ProfileCreateView(generics.ListCreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = CreateProfileSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = None

#     def get_queryset(self):
#         return super().get_queryset()

#     # def list(self, request, *args, **kwargs):
#     #     qs = Profile.objects.filter(user=request.user)
#     #     return qs
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset().filter(user=request.user)
#         queryset = self.filter_queryset(queryset)

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return response.Response(serializer.data)

#     def perform_create(self, serializer):
#         serializer.save(active=True)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return response.Response(
#                 serializer.data, status=status.HTTP_201_CREATED, headers=headers
#             )
#         except Exception as e:
#             # print(e)

#             return response.Response(
#                 {
#                     "detail": f"Failed to create a profile, user already have requested profile"
#                 },
#                 status=status.HTTP_409_CONFLICT,
#             )


# class LoginView(generics.GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserAccountSerializer

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         password = request.data.get("password")
#         user = authenticate(email=email, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         else:
#             return Response({"detail": "Invalid credentials"}, status=400)
        
# class MeView(generics.RetrieveAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = MeSerializer
    
#     def get_queryset(self):
#         return UserAccount.objects.filter().prefetch_related('profiles')
#     def get_object(self):
#         return self.request.user