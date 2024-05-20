from .serializers import InstitutionSerializer, InstitutionRetrieveSerializer
from .models import Institution
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework import status

# Create your views here.


class CreateInstitutionView(CreateAPIView):
    permission_classes = []
    serializer_class = InstitutionSerializer
    queryset = Institution.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Institution created successfully",
                    "data": serializer.data,
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(
                {
                    "message": "Failed to create institution, Validation error occurred.",
                    "error": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "message": "Failed to create institution. Exception error occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllInstitutions(ListAPIView):
    permission_classes = []
    serializer_class = InstitutionRetrieveSerializer
    queryset = Institution.objects.all()


class InstitutionReadUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = InstitutionRetrieveSerializer
    queryset = Institution.objects.all()
