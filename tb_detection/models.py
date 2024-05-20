from django.db import models
from patient.models import Patient


class TbDetection(models.Model):
    TB_STATUS = (
        ("Infected", "Infected"),
        ("Not Infected", "Not Infected"),
    )
    patient = models.ForeignKey(
        Patient, related_name="tb_detections", on_delete=models.CASCADE
    )
    date_tested = models.DateField(auto_now_add=True, null=True, blank=True)
    input_image = models.ImageField(upload_to="input_images/", null=True, blank=True)
    tb_status = models.CharField(
        max_length=100, blank=True, null=True, choices=TB_STATUS
    )
    output_image_mask = models.ImageField(
        upload_to="output_image_masks/", null=True, blank=True
    )

    def __str__(self):
        return f"{self.patient.user.first_name} {self.patient.user.last_name}"
