from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import CameraSetting
from api.serializers import CameraSettingSerializer


class GetCameraSetting(APIView):

    def get(self, request):
        settings = CameraSetting.get_settings()
        serializer = CameraSettingSerializer(settings)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
