from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import FlashSetting
from api.serializers import FlashSettingSerializer


class UpdateFlashSetting(APIView):

    def patch(self, request):
        settings = FlashSetting.get_settings()

        serializer = FlashSettingSerializer(settings, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"status": {"code": 0, "message": "update success"}, "data": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(
            data={"status": {"code": 1, "message": "validation error"}, "errors": serializer.errors},
            status=status.HTTP_200_OK
        )


