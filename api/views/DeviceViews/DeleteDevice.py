from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Device

class DeleteDevice(APIView):

    def delete(self, request, device_id=None):
        if device_id is None:
            return Response(
                data={"status": {"code": 1, "message": "device_id required"}, "data": {}},
                status=status.HTTP_200_OK
            )

        device = Device.objects.filter(id=device_id).first()
        if not device:
            return Response(
                data={"status": {"code": 3, "message": "device not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        device.delete()

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": {}},
            status=status.HTTP_200_OK
        )
