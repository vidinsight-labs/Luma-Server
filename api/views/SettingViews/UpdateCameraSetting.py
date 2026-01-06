from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import CameraSetting, Device
from api.serializers import CameraSettingSerializer
from api.utils import set_device_settings


class UpdateCameraSetting(APIView):

    def patch(self, request):
        settings = CameraSetting.get_settings()

        serializer = CameraSettingSerializer(settings, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            settings.refresh_from_db()

            devices = Device.objects.all()

            try:
                device_responses = set_device_settings(devices, settings)

                return Response(
                    data={
                        "status": {"code": 0, "message": "update success"},
                        "data": {
                            **serializer.data,
                            "device_responses": device_responses
                        }
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    data={
                        "status": {"code": 0, "message": f"settings updated but failed to send to devices: {str(e)}"},
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

        return Response(
            data={"status": {"code": 1, "message": "validation error"}, "errors": serializer.errors},
            status=status.HTTP_200_OK
        )