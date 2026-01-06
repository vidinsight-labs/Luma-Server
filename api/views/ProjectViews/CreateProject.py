import os
from django.db import IntegrityError, transaction
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Project
from api.serializers import ProjectSerializer


class CreateProject(APIView):

    def post(self, request):
        name = request.data.get('name')

        missing = []
        if not name:
            missing.append('name')

        if missing:
            return Response(
                data={"status": {"code": 1, "message": f"Missing fields: {', '.join(missing)}"}, "data": {}},
                status=status.HTTP_200_OK
            )

        if Project.objects.filter(name=name).exists():
            return Response(
                data={"status": {"code": 1, "message": "this project name already exists"}, "data": {}},
                status=status.HTTP_200_OK
            )

        project_path = os.path.join(
            settings.BASE_DIR,
            settings.PROJECT_DIR,
            name
        )

        # Project klasörünü oluştur
        try:
            os.makedirs(project_path, exist_ok=True)
        except OSError as e:
            return Response(
                data={"status": {"code": 1, "message": f"Failed to create directory: {str(e)}"}, "data": {}},
                status=status.HTTP_200_OK
            )

        try:
            with transaction.atomic():
                project = Project.objects.create(
                    name=name,
                    path=project_path
                )
        except IntegrityError:
            return Response(
                data={"status": {"code": 1, "message": "conflict on unique fields"}, "data": {}},
                status=status.HTTP_200_OK
            )

        serializer = ProjectSerializer(project)
        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )