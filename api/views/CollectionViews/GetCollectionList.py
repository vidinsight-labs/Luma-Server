from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Collection, Project
from api.serializers import CollectionSerializer


class GetCollectionList(APIView):

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

        collections = Collection.objects.filter(project=project).order_by('-created_at')
        serializer = CollectionSerializer(collections, many=True)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
