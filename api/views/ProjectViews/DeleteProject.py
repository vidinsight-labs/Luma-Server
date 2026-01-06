import os
import shutil
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Project


class DeleteProject(APIView):

    def delete(self, request, project_id=None):
        if project_id is None:
            return Response(
                data={"status": {"code": 1, "message": "project_id required"}, "data": {}},
                status=status.HTTP_200_OK
            )

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response(
                data={"status": {"code": 3, "message": "project not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        project_path = project.path
        project.delete()

        if project_path and os.path.exists(project_path):
            try:
                shutil.rmtree(project_path)
            except Exception as e:
                pass

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": {}},
            status=status.HTTP_200_OK
        )