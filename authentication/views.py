from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers import ProfileSerializer, CreateProfileSerializer
from authentication.models import Profile


class SignupView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


class ProfileCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset()

    # def list(self, request, *args, **kwargs):
    #     qs = Profile.objects.filter(user=request.user)
    #     return qs
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            # print(e)

            return response.Response(
                {
                    "detail": f"Failed to create a profile, user already have requested profile"
                },
                status=status.HTTP_409_CONFLICT,
            )
