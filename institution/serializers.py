from institution.models import Institution
from rest_framework.serializers import ModelSerializer


class InstitutionSerializer(ModelSerializer):

    class Meta:
        model = Institution
        exclude = ['institution_number']

        extra_kwargs = {
            "institution_name": {"required": True},
            "institution_code": {"required": True},
            "institution_type": {"required": True},
            "institution_address": {"required": True},
            "phone_number": {"required": True},
        }


class InstitutionRetrieveSerializer(ModelSerializer):

    class Meta:
        model = Institution
        fields = "__all__"

        
class MinimizedInstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'institution_name']