from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import FlashSetting
from api.serializers import FlashSettingSerializer


class GetFlashSetting(APIView):

    def get(self, request):
        settings = FlashSetting.get_settings()
        serializer = FlashSettingSerializer(settings)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )


