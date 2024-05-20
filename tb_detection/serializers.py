from rest_framework import serializers
from .models import TbDetection
from patient.models import Patient


class TbDetectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TbDetection
        exclude = ["tb_status", "output_image_mask"]

        extra_kwargs = {
            "patient": {"required": True},
            "input_image": {"required": True},
        }

    def update(self, instance, validated_data):
        instance.patient = validated_data.get("patient", instance.patient)
        instance.date_tested = validated_data.get("date_tested", instance.date_tested)
        instance.input_image = validated_data.get("input_image", instance.input_image)
        instance.tb_status = validated_data.get("tb_status", instance.tb_status)
        instance.output_image_mask = validated_data.get(
            "output_image_mask", instance.output_image_mask
        )
        instance.save()
        return instance

class TbDetectionRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = TbDetection
        fields = '__all__'
        depth=2
