from rest_framework.serializers import ModelSerializer
from .models import Administrator
from accounts.serializers import UserSerializer, RetrieveUserSerializer
from accounts.models import User
from django.contrib.auth.models import Group, Permission


class AdministratorSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Administrator
        fields = "__all__"

        extra_kwargs = {
            "user": {"write_only": True},
            "status": {"required": True},
            "employment_status": {"required": True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        groups_data = user_data.pop("groups", [])
        permissions_data = user_data.pop("user_permissions", [])

        user = User.objects.create(**user_data)

        user.role = "ADMIN"
        user.is_superuser = False
        user.is_staff = True
        user.is_active = True
        total_administrators = Administrator.objects.filter(
            user__institution_id=user_data["institution"]
        ).count()
        new_username = f"{user.username}{total_administrators}A"
        user.username = new_username
        user.set_password("ADMIN")

        try:
            admin = Administrator.objects.create(user=user, **validated_data)
            user.save()

            groups = Group.objects.filter(
                id__in=[group_data["id"] for group_data in groups_data]
            )
            admin.user.groups.set(groups)

            permissions = Permission.objects.filter(
                id__in=[perm_data["id"] for perm_data in permissions_data]
            )
            admin.user.user_permissions.set(permissions)

            admin.save()
            return admin

        except Exception as e:
            user.delete()  # Delete the user if Admin creation fails
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


class AdministratorRetrieveSerializer(ModelSerializer):
    user = RetrieveUserSerializer()

    class Meta:
        model = Administrator
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
