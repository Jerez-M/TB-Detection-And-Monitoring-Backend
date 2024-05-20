from django.urls import path
from . import views

urlpatterns = [
    path("detect/", views.TbDetectionCreateView.as_view(), name="tb-detection-create-view"),
    path(
        "<int:pk>/",
        views.TbDetectionRetrieveUpdateDestroyView.as_view(),
        name="tb-detection-retrieve-update-destroy",
    ),
    path(
        "get-all-by-institution-id/<int:institution_id>/",
        views.TbDetectionListCreateView.as_view(),
        name="get-all",
    ),
]
