from django.urls import path

from . import views

urlpatterns = [
    path('submissions/', views.SubmissionsView.as_view(), name='create_submission'),
    path('submissions/<uuid:submission_uuid>/', views.SubmissionView.as_view(), name='get_submission'),
]
