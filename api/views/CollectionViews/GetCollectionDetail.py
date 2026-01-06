from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Collection
from api.serializers import CollectionSerializer


class GetCollectionDetail(APIView):

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

        serializer = CollectionSerializer(collection)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )
