import os
import zipfile
import tempfile
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Project, Collection, File


class DownloadProject(APIView):

    def get(self, request, project_id=None):
        if project_id is None:
            return Response(
                data={"status": {"code": 1, "message": "project_id required"}, "data": {}},
                status=status.HTTP_200_OK
            )

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response(
                data={"status": {"code": 2, "message": "project not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        collections = Collection.objects.filter(project=project)

        if not collections.exists():
            return Response(
                data={"status": {"code": 3, "message": "project has no collections"}, "data": {}},
                status=status.HTTP_200_OK
            )

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_file.close()

        try:
            with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for collection in collections:
                    files = File.objects.filter(collection=collection)

                    for file_obj in files:
                        file_path = file_obj.path

                        if not os.path.exists(file_path):
                            file_path = os.path.join(collection.path, file_obj.name)

                        if os.path.exists(file_path):
                            arcname = os.path.join(project.name, collection.name, file_obj.name)
                            zip_file.write(file_path, arcname=arcname)

            zip_file_handle = open(temp_file.name, 'rb')
            response = FileResponse(
                zip_file_handle,
                content_type='application/zip',
                as_attachment=True,
                filename=f'{project.name}.zip'
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
