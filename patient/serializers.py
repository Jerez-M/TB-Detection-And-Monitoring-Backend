from rest_framework import serializers
from .models import Patient
from accounts.models import User
from django.contrib.auth.models import Group, Permission


class PatientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["role", "is_superuser", "is_staff", "is_active", "institution_email", "password"]

        extra_kwargs = {
            "institution": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "gender": {"required": True},
            "phone_number_1": {"required": True},
            "national_id": {"required": True},
            "nationality": {"required": True},
            "home_address": {"required": True},
            "altEmail": {"required": True},
        }


class RetrievePatientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["institution_email", "password"]


class PatientSerializer(serializers.ModelSerializer):
    user = PatientUserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        groups_data = user_data.pop("groups", [])
        permissions_data = user_data.pop("user_permissions", [])

        user = User.objects.create(**user_data)

        user.role = "PATIENT"
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        password = "password"
        user.set_password(password)

        try:
            patient = Patient.objects.create(user=user, **validated_data)
            user.save()

            groups = Group.objects.filter(
                id__in=[group_data["id"] for group_data in groups_data]
            )
            patient.user.groups.set(groups)

            permissions = Permission.objects.filter(
                id__in=[perm_data["id"] for perm_data in permissions_data]
            )
            patient.user.user_permissions.set(permissions)

            patient.save()
            return patient

        except Exception as e:
            user.delete()  # Delete the user if patient creation fails
            raise e  # Re-raise the exception

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        groups_data = user_data.pop("groups", [])
        permissions_data = user_data.pop("user_permissions", [])

        if user_data:
            user = instance.user
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()

        if groups_data:
            groups = Group.objects.filter(
                id__in=[group_data["id"] for group_data in groups_data]
            )
            instance.user.groups.set(groups)

        if permissions_data:
            permissions = Permission.objects.filter(
                id__in=[perm_data["id"] for perm_data in permissions_data]
            )
            instance.user.user_permissions.set(permissions)

        return super().update(instance, validated_data)


class PatientRetrieveSerializer(serializers.ModelSerializer):
    user = RetrievePatientUserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        groups_data = user_data.pop("groups", [])
        permissions_data = user_data.pop("user_permissions", [])

        if user_data:
            user = instance.user
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()

        if groups_data:
            groups = Group.objects.filter(
                id__in=[group_data["id"] for group_data in groups_data]
            )
            instance.user.groups.set(groups)

        if permissions_data:
            permissions = Permission.objects.filter(
                id__in=[perm_data["id"] for perm_data in permissions_data]
            )
            instance.user.user_permissions.set(permissions)

        return super().update(instance, validated_data)


class PatientUploadProfPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient", "file"]
