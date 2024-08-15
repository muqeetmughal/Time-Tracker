from django.urls import path
from django.contrib.auth import views as auth_views
from authentication.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('pro/', dashboard_view, name='profile'),
    
    path('logout/',user_logout, name='logout' ),
    path('users/', user_list_view, name='user_list'),
    
    path('update/<int:pk>/', update_user, name='user_update'),
    path('delete/<int:pk>/', delete_user, name='user_delete'),
    


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    #-----------------------------------------------------------------------------------------------------------
    
    # path('signup/', SignupView.as_view(), name='signup'),
    # path('profile/create/', ProfileCreateView.as_view(), name='signup'),
    # path('me/', MeView.as_view(), name='me'),
    # path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
