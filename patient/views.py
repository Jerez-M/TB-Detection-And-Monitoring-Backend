from .serializers import PatientSerializer, PatientRetrieveSerializer
from .models import Patient
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import status
from accounts.models import User
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class CreatePatientView(CreateAPIView):
    permission_classes = []
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def create(self, request, *args, **kwargs):
        
        password="password"
        serializer = self.get_serializer(data=request.data)
        
        try:
            if serializer.is_valid():

                self.perform_create(serializer)
                data = {
                    "message": "Patient created successfully",
                    "data": serializer.data
                }

                first_name = serializer.validated_data['user']['first_name'].upper()
                last_name = serializer.validated_data['user']['last_name'].upper()
                username = serializer.validated_data['user']['username']
                altEmail = serializer.validated_data['user']['altEmail']
                role = 'PATIENT'
                full_name = f'{first_name } { last_name}'

                email_subject = f"Welcome to the Hospital's Portal, Your Account has been Created Successfully"
                email_to = serializer.validated_data['user']['altEmail']
                email_from = settings.EMAIL_HOST_USER
                email_body = f"Dear {full_name},\n\nWe are delighted to inform you that your account has been successfully created for the Hospital's Portal. " \
                            f"You can now access your account using the following details:\n\n" \
                            f"Username: {username}\n" \
                            f"Password: {password}\n"\
                            f"Email: {altEmail}\n" \
                            f"Role: {role}\n\n" \
                            f"Kindly use the Username and password above to Sign in to your account. \n \n" \
                            f"Please keep this information secure and do not share it with anyone. If you have any questions or need assistance, " \
                            f"feel free to reach out to our support team at +263783382395.\n\n" \
                            f"Thank you for joining Hospital's Portal. We look forward to providing you with a great experience!\n\n" \
                            f"Best regards,\n" \
                            f"System Administrator\n"  
                                                          
                send_mail(email_subject, email_body, email_from, [email_to], fail_silently=True)
                return Response(data, status=status.HTTP_201_CREATED)

            return Response({"message": "Failed to create patient, Validation error occurred.", "error": serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": "Failed to create patient. Exception error occurred", "error": str(e)}, 
                            status=status.HTTP_400_BAD_REQUEST)
        

class GetAllPatients(ListAPIView):
    permission_classes = []
    serializer_class = PatientRetrieveSerializer
    queryset = Patient.objects.all()


class PatientReadUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = PatientRetrieveSerializer
    queryset = Patient.objects.all()