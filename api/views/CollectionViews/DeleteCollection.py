import os
import shutil
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Collection


class DeleteCollection(APIView):

    def delete(self, request, collection_id=None):
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

        collection_path = collection.path

        collection.delete()

        if collection_path and os.path.exists(collection_path):
            try:
                shutil.rmtree(collection_path)
            except Exception as e:
                pass

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": {}},
            status=status.HTTP_200_OK
        )
