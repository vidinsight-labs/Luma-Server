import os
import zipfile
import tempfile
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Collection, File


class DownloadCollection(APIView):

    def get(self, request, collection_id=None):
        if collection_id is None:
            return Response(
                data={"status": {"code": 1, "message": "collection_id required"}, "data": {}},
                status=status.HTTP_200_OK
            )

        collection = Collection.objects.filter(id=collection_id).first()
        if not collection:
            return Response(
                data={"status": {"code": 2, "message": "collection not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        files = File.objects.filter(collection=collection)

        if not files.exists():
            return Response(
                data={"status": {"code": 3, "message": "collection has no files"}, "data": {}},
                status=status.HTTP_200_OK
            )

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_file.close()

        try:
            with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_obj in files:
                    file_path = file_obj.path

                    if not os.path.exists(file_path):
                        file_path = os.path.join(collection.path, file_obj.name)

                    if os.path.exists(file_path):
                        zip_file.write(file_path, arcname=file_obj.name)

            zip_file_handle = open(temp_file.name, 'rb')
            response = FileResponse(
                zip_file_handle,
                content_type='application/zip',
                as_attachment=True,
                filename=f'{collection.name}.zip'
            )

            return response

        except Exception as e:
            try:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
            except:
                pass

            return Response(
                data={"status": {"code": 1, "message": f"Failed to create zip: {str(e)}"}, "data": {}},
                status=status.HTTP_200_OK
            )