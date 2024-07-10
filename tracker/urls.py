from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# router.register(r"user", UserAccountViewSet, basename="customuser")
router.register(r"project", ProjectViewSet, basename="project")
router.register(r"activity", ActivityViewSet, basename="activity")
router.register(r"member", MemberViewSet, basename="member")
router.register(r"artifact", ArtifactViewSet, basename="artifact")



urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name="logout"),
    path('', include(router.urls)),
    
] 
urlpatterns += router.urls
