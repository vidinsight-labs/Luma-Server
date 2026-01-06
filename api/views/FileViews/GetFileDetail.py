from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import File
from api.serializers import FileSerializer

class GetFileDetail(APIView):

    def get(self, request, file_id=None):
        if file_id is None:
            return Response(
                data={"status": {"code": 1, "message": "file_id required"}, "data": {}},
                status=status.HTTP_200_OK
            )

        file = File.objects.filter(id=file_id).first()
        if not file:
            return Response(
                data={"status": {"code": 3, "message": "file not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        serializer = FileSerializer(file)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
