from .serializers import AdministratorSerializer, AdministratorRetrieveSerializer
from .models import Administrator
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User

# Create your views here.


class CreateAdministratorView(CreateAPIView):
    permission_classes = []
    serializer_class = AdministratorSerializer
    queryset = Administrator.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:

            if serializer.is_valid():
                self.perform_create(serializer)
                data = {
                    "message": "Administrator created successfully",
                    "data": serializer.data
                }

                first_name = serializer.validated_data['user']['first_name'].upper()
                last_name = serializer.validated_data['user']['last_name'].upper()
                altEmail = serializer.validated_data['user']['altEmail']
                institution_email = serializer.validated_data['user']['institution_email']
                full_name = f'{first_name } { last_name}'
                password = 'ADMIN'

                this_instance = User.objects.get(pk=serializer.data['user']['id'])
                username = this_instance.username
                role = this_instance.role


                email_subject = f"Welcome to the Hospital's Portal, Your Account has been Created Successfully"
                email_to = institution_email
                email_to_2 = altEmail
                email_from = settings.EMAIL_HOST_USER
                email_body = f"Dear {full_name},\n\nWe are delighted to inform you that your account has been successfully created for the Hospital's Portal. " \
                            f"You can now access your account using the following details:\n\n" \
                            f"Username: {username}\n" \
                            f"Password: {password}\n"\
                            f"Institution Email: {institution_email}\n" \
                            f"Personal Email: {altEmail}\n" \
                            f"Role: {role}\n\n" \
                            f"Kindly use the Username and password above to Sign in to your account. \n \n" \
                            f"Please keep this information secure and do not share it with anyone. If you have any questions or need assistance, " \
                            f"feel free to reach out to our support team at +263783382395.\n\n" \
                            f"Thank you for joining Hospital's Portal. We look forward to providing you with a great experience!\n\n" \
                            f"Best regards,\n" \
                            f"System Administrator\n"  
                                                          
                send_mail(email_subject, email_body, email_from, [email_to, email_to_2], fail_silently=True)

                return Response(data, status=status.HTTP_201_CREATED)

            return Response({"message": "Failed to create administrator, Validation error occurred.", "error": serializer.errors}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": "Failed to create administrator. Exception error occurred", "error": str(e)}, 
                            status=status.HTTP_400_BAD_REQUEST)
        

class GetAllAdministrators(ListAPIView):
    permission_classes = []
    serializer_class = AdministratorRetrieveSerializer
    queryset = Administrator.objects.all()


class AdministratorReadUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    serializer_class = AdministratorRetrieveSerializer
    queryset = Administrator.objects.all()

