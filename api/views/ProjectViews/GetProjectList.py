from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Project
from api.serializers import ProjectSerializer

class GetProjectList(APIView):

    def get(self, request):
        projects = Project.objects.all()

        serializer = ProjectSerializer(projects, many=True)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
