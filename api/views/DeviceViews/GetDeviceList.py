from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Device
from api.serializers import DeviceSerializer
from api.utils import get_device_data

class GetDeviceList(APIView):

    def get(self, request):
        devices = Device.objects.all()

        for device in devices:
            response = get_device_data(device.ip)
            device.cameras = response.get("cameras")
            device.statistics = response.get("device").get("statistics")
            device.save()

        serializer = DeviceSerializer(devices, many=True)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
