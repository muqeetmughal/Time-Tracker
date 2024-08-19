from .models import *
from .serializers import *
from .forms import *
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.db.models import *
from django.db.models.functions import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
# from tracker.filters import ActivityFilter
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework.decorators import action
# from authentication.models import Profile
import django_filters.rest_framework as filters
from rest_framework.exceptions import ValidationError

UserAccount = get_user_model()



#----------------------------------Orgnizations--------------------------------------------


@login_required
def organization_list(request):
    orgnization = Organization.objects.filter(owner = request.user)
    if len(orgnization) >0:
        organizations = Organization.objects.all()
        return render(request, 'orgnization/organization_list.html', {'organizations': organizations})
    return redirect('organization_create')


@login_required
def organization_create(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.owner = request.user
            organization.save()
            organization.members.add(request.user)
            
            return redirect('organization_list')
    else:
        form = OrganizationForm()
    return render(request, 'orgnization/organization_form.html', {'form': form})



@login_required
def organization_update(request, pk):
    orgnisation = Organization.objects.filter(owner = request.user)
    if len(orgnisation) >0:
        
        organization = get_object_or_404(Organization, pk=pk)
        if request.user != organization.owner:
            return HttpResponseForbidden()
        if request.method == 'POST':
            form = OrganizationForm(request.POST, instance=organization)
            if form.is_valid():
                form.save()
                return redirect('organization_list')
        else:
            form = OrganizationForm(instance=organization)
        return render(request, 'orgnization/organization_form.html', {'form': form})
    
    return redirect('user_list')



@login_required
def organization_delete(request, pk):
    orgnisation = Organization.objects.filter(owner = request.user)
    if len(orgnisation) >0:
        
        organization = get_object_or_404(Organization, pk=pk)
        if request.user != organization.owner:
            return HttpResponseForbidden()
        if request.method == 'POST':
            organization.delete()
            return redirect('organization_list')

        return render(request, 'orgnization/organization_confirm_delete.html', {'object': organization})
    
    return redirect('user_list')



#----------------------------------Projects--------------------------------------------


@login_required
def project_list(request):
    projects = Project.objects.filter(projectmember__user = request.user)
    return render(request, 'project/project_list.html', {'projects': projects})



@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render( request, 'project/project_form.html', {'form': form})










































































































# class UserAccountViewSet(viewsets.ModelViewSet):
#     queryset = UserAccount.objects.all()
#     serializer_class = UserAccountSerializer


# class ProjectViewSet(viewsets.ModelViewSet):
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):

#         qs = Project.objects.all()
#         if self.action == "list":
#             # qs = qs.filter(
#             #     created_by=self.request.user.profiles.filter(active=True).first()
#             # )
#             qs = qs.select_related("created_by__user")
#             qs = qs.prefetch_related("engagements")

#             # qs = qs.filter(
#             #     engagements__profile__user=self.request.user, engagements__is_active=True
#             # ).distinct()
#             qs = qs.annotate(
#                 created_by_name=F("created_by__name"),
#                 created_by_user_email=F("created_by__user__email"),
#                 # project_role=F("engagements__role"),
#                 members_count=Count(
#                     "engagements__profile",
#                     filter=Q(engagements__is_active=True),
#                     distinct=True,
#                 ),
#             )

#             qs = qs.order_by("-updated_at")
#         # for project in qs:
#         #     print(f"Project: {project.name}, Members Count: {project.members_count}, Created By: {project.created_by__user__email}, Project Role: {project.project_role}")

#         return qs

#     def perform_create(self, serializer):
#         profile = self.request.user.profiles.filter(active=True).first()
#         if not profile:
#             raise ValidationError({"detail": "No profile found for account"})
#         serializer.save(created_by=profile)

#     def send_invites(self):
#         # [
#         #     {
#         #         "email": "saad@infintrixtech.com",
#         #         "rate": "15",
#         #         "role": "worker"
#         #     },
#         #     {
#         #         "email": "abdulmuqeetwork@gmail.com",
#         #         "rate": "10",
#         #         "role": "supervisor"
#         #     }
#         # ]
#         return


# class ActivityViewSet(viewsets.ModelViewSet):
#     serializer_class = ActivitySerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.DjangoFilterBackend]
#     filterset_class = ActivityFilter

#     def get_queryset(self):
#         # user=self.request.user
#         qs = Activity.objects.filter()
#         # .annotate(project_name=F("project__name"))
#         return qs

#     def perform_create(self, serializer):
#         # print(serializer.validated_data)

#         # print(project.engagements.filter(profile__user=self.request.user).first())
#         if isinstance(serializer.validated_data, list):
#             # Bulk create if serializer data is a list
#             activities_to_create = []
#             for activity in serializer.validated_data:
#                 membership = (
#                     activity["project"]
#                     .engagements.filter(profile__user=self.request.user)
#                     .first()
#                 )
#                 activity = Activity(**activity)
#                 activity.member = membership
#                 activities_to_create.append(activity)
#             Activity.objects.bulk_create(activities_to_create)
#         else:
#             membership = (
#                 serializer.validated_data["project"]
#                 .engagements.filter(profile__user=self.request.user)
#                 .first()
#             )
#             # Single object creation
#             serializer.save(member=membership)

#     def create(self, request, *args, **kwargs):
#         if isinstance(request.data, list):
#             # If request data is a list, many=True for bulk create
#             serializer = self.get_serializer(data=request.data, many=True)
#         else:
#             # Otherwise, treat as a single object
#             serializer = self.get_serializer(data=request.data)

#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {"detail": "Activities created successfully"},
#             status=status.HTTP_201_CREATED,
#             headers=headers,
#         )


# class MembershipViewSet(viewsets.ModelViewSet):
#     queryset = Membership.objects.all()
#     serializer_class = MemberSerializer

#     # custom action list current user invitation


# class ShotViewSet(viewsets.ModelViewSet):
#     queryset = Shot.objects.all()
#     serializer_class = ShotSerializer
