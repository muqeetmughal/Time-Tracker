from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

# router.register(r"user", UserAccountViewSet, basename="customuser")
# router.register(r"projects", ProjectViewSet, basename="project")
# router.register(r"activities", ActivityViewSet, basename="activity")
# router.register(r"members", MembershipViewSet, basename="member")
# router.register(r"shots", ShotViewSet, basename="artifact")



urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name="logout"),
    # path('', include(router.urls)),
    
    path('organizations/', organization_list, name='organization_list'),
    path('organizations/create/', organization_create, name='organization_create'),
    path('organizations/<int:pk>/update/', organization_update, name='organization_update'),
    path('organizations/<int:pk>/delete/', organization_delete, name='organization_delete'),
    
    
    path('projects/', project_list, name='project_list'),
    path('project/create/', project_create, name='project_create'),
    # path('organizations/<int:pk>/update/', organization_update, name='organization_update'),
    # path('organizations/<int:pk>/delete/', organization_delete, name='organization_delete'),
    
    
] 
urlpatterns += router.urls
