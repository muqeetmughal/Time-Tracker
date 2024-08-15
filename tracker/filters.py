from rest_framework.filters import SearchFilter
import django_filters.rest_framework as filters
# from tracker.models import Activity, Project


# class ActivityFilter(filters.FilterSet):
#     project = filters.ModelMultipleChoiceFilter(
#         field_name='project',
#         queryset=Project.objects.filter(),  # Set default empty queryset
#         label='Project Names'
#     )

#     class Meta:
#         model = Activity
#         fields = ['project']