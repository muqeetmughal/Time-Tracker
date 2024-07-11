from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# router.register(r"user", UserAccountViewSet, basename="customuser")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"activities", ActivityViewSet, basename="activity")
router.register(r"members", MembershipViewSet, basename="member")
router.register(r"shots", ShotViewSet, basename="artifact")



urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name="logout"),
    path('', include(router.urls)),
    
] 
urlpatterns += router.urls
