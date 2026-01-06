from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Device
from api.utils import reconnect_cameras


class ReconnectCameras(APIView):

    def post(self, request):
        devices = Device.objects.all()

        if not devices.exists():
            return Response(
                data={"status": {"code": 1, "message": "no devices found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        try:
            device_responses = reconnect_cameras(devices)

            return Response(
                data={
                    "status": {"code": 0, "message": "reconnect cameras request sent"},
                    "data": {
                        "device_responses": device_responses
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={
                    "status": {"code": 1, "message": f"failed to reconnect cameras: {str(e)}"},
                    "data": {}
                },
                status=status.HTTP_200_OK
            )