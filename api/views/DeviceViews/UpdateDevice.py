from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Device
from api.serializers import DeviceSerializer


class UpdateDevice(APIView):
    
    def patch(self, request, device_id=None):
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

        serializer = DeviceSerializer(device, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"status": {"code": 0, "message": "partial update success"}, "data": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(
            data={"status": {"code": 2, "message": "validation error"}, "errors": serializer.errors},
            status=status.HTTP_200_OK
        )
