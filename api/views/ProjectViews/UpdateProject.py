from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Project
from api.serializers import ProjectSerializer


class UpdateProject(APIView):

    def patch(self, request, project_id=None):
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

        serializer = ProjectSerializer(project, data=request.data, partial=True)

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
