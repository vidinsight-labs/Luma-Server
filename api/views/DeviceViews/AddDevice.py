from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Device
from api.serializers import DeviceSerializer
from api.utils import get_device_data


class AddDevice(APIView):

    def post(self, request):
        name = request.data.get('name')
        ip = request.data.get('ip')

        missing = []
        if not name:
            missing.append('name')
        if not ip:
            missing.append('serial_number')

        if missing:
            return Response(
                data={"status": {"code": 1, "message": f"Missing fields: {', '.join(missing)}"}, "data": {}},
                status=status.HTTP_200_OK
            )

        if Device.objects.filter(name=name).exists():
            return Response(
                data={"status": {"code": 1, "message": "this device name already exists"}, "data": {}},
                status=status.HTTP_200_OK
            )

        if Device.objects.filter(ip=ip).exists():
            return Response(
                data={"status": {"code": 1, "message": "this device already exists"}, "data": {}},
                status=status.HTTP_200_OK
            )

        data = get_device_data(ip)

        try:
            with transaction.atomic():
                device = Device.objects.create(
                    name=name,
                    device_id=data.get('device').get('device_id'),
                    ip=ip,
                    cameras=data.get('cameras'),
                    statistics=data.get('device').get('statistics'),
                )
        except IntegrityError:
            return Response(
                data={"status": {"code": 1, "message": "conflict on unique fields"}, "data": {}},
                status=status.HTTP_200_OK
            )

        serializer = DeviceSerializer(device)
        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
