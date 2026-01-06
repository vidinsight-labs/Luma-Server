import os
import mimetypes
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import File


class DownloadFile(APIView):

    def get(self, request, file_id=None):
        if file_id is None:
            return Response(
                data={"status": {"code": 1, "message": "file_id required"}, "data": {}},
                status=status.HTTP_200_OK
            )

        file_obj = File.objects.filter(id=file_id).first()
        if not file_obj:
            return Response(
                data={"status": {"code": 2, "message": "file not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        file_path = file_obj.path

        if not os.path.exists(file_path):
            file_path = os.path.join(file_obj.collection.path, file_obj.name)

        if not os.path.exists(file_path):
            return Response(
                data={"status": {"code": 3, "message": "file not found on filesystem"}, "data": {}},
                status=status.HTTP_200_OK
            )

        try:
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'

            file_handle = open(file_path, 'rb')
            response = FileResponse(
                file_handle,
                content_type=content_type,
                as_attachment=True,
                filename=file_obj.name
            )

            return response

        except Exception as e:
            return Response(
                data={"status": {"code": 1, "message": f"Failed to read file: {str(e)}"}, "data": {}},
                status=status.HTTP_200_OK
            )
