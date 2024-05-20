import os
from django.conf import settings
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from rest_framework import generics
from .models import TbDetection
from .serializers import TbDetectionSerializer, TbDetectionRetrieveSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


# class TbDetectionCreateView(generics.GenericAPIView):
#     permission_classes = []
#     serializer_class = TbDetectionSerializer
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()

#         except Exception as e:
#             return Response(
#                 {
#                     "message": "Tb detection failed, Exception occurred.",
#                     "error": {"message": [str(e)]},
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         else:
#             return Response(
#                 {
#                     "message": "Tb detection completed successfully",
#                     "status": "Infected",
#                     "data": serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )


class TbDetectionCreateView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = TbDetectionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classification_model = None
        self.segmentation_model = None
        self.load_models()

    def load_models(self):
        # Load the pre-trained classification model
        classification_model_path = os.path.join(
            settings.BASE_DIR, "machine_learning_models", "classification_model.keras"
        )
        self.classification_model = load_model(classification_model_path)

        # Load the pre-trained segmentation model
        segmentation_model_path = os.path.join(
            settings.BASE_DIR,
            "machine_learning_models",
            "unet_segmentation_model.keras",
        )
        self.segmentation_model = load_model(segmentation_model_path)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                input_image = serializer.validated_data["input_image"]
                patient = serializer.validated_data["patient"]

                # Preprocess the input image for the classification model
                image = Image.open(input_image)
                image = image.resize(
                    (224, 224)
                )  # Assuming the classification model expects 224x224 input
                image_array = np.array(image) / 255.0  # Normalize the pixel values
                image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

                # Classify the input image
                classification_result = self.classification_model.predict(image_array)[
                    0
                ][0]
                if classification_result < 0.5:
                    tb_status = "Not Infected"
                else:
                    tb_status = "Infected"

                # If the image is infected, run the segmentation model
                if tb_status == "Infected":
                    segmentation_result = self.segmentation_model.predict(image_array)[
                        0
                    ]
                    segmentation_image = Image.fromarray(
                        (segmentation_result * 255).astype(np.uint8)
                    )
                    segmentation_image.save(
                        os.path.join(
                            settings.MEDIA_ROOT,
                            "output_image_masks",
                            f"{patient.id}.png",
                        )
                    )
                    serializer.validated_data["output_image_mask"] = (
                        f"output_image_masks/{patient.id}.png"
                    )
                else:
                    serializer.validated_data["output_image_mask"] = None

                serializer.validated_data["tb_status"] = tb_status
                serializer.save()

        except Exception as e:
            return Response(
                {
                    "message": "Tb detection failed, Exception occurred.",
                    "error": {"message": [str(e)]},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {
                    "message": "Tb detection completed successfully",
                    "status": tb_status,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )


class TbDetectionListCreateView(generics.ListAPIView):
    queryset = TbDetection.objects.all()
    serializer_class = TbDetectionRetrieveSerializer


class TbDetectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TbDetection.objects.all()
    serializer_class = TbDetectionRetrieveSerializer


class GetAllByInstitutionId(generics.GenericAPIView):
    serializer_class = TbDetectionRetrieveSerializer
    permission_classes = []
