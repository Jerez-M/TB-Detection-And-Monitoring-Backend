from django.urls import path
from institution import views

urlpatterns = [
    path("", views.CreateInstitutionView.as_view(), name="create_institution"),
    path("<int:pk>/", views.InstitutionReadUpdateDestroyView.as_view()),
    path("get-all/", views.GetAllInstitutions.as_view()),
]
