from django.urls import path
from authentication.views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/create/', ProfileCreateView.as_view(), name='signup'),
]
