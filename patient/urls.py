from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreatePatientView.as_view(), name="create_patient"),
    path("<int:pk>/", views.PatientReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllPatients.as_view()),
    # path('update-patient-profile-picture-using-patient-id/<int:Id>/', views.Update_staff_profile_picture.as_view()),
]
