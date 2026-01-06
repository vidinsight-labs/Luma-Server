import os
from django.db import IntegrityError, transaction
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Collection, Project, Device, File, FlashSetting
from api.serializers import CollectionSerializer
from api.utils import get_photo_list, get_device_photo, trigger


class CreateCollection(APIView):

    def post(self, request, project_id=None):
        name = request.data.get('name')

        missing = []
        if not name:
            missing.append('name')
        if not project_id:
            missing.append('project_id')

        if missing:
            return Response(
                data={"status": {"code": 1, "message": f"Missing fields: {', '.join(missing)}"}, "data": {}},
                status=status.HTTP_200_OK
            )

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return Response(
                data={"status": {"code": 2, "message": "project not found"}, "data": {}},
                status=status.HTTP_200_OK
            )

        if Collection.objects.filter(name=name, project=project).exists():
            return Response(
                data={"status": {"code": 1, "message": "this collection name already exists"}, "data": {}},
                status=status.HTTP_200_OK
            )

        collection_path = os.path.join(
            settings.BASE_DIR,
            settings.PROJECT_DIR,
            project.name,
            name
        )

        try:
            os.makedirs(collection_path, exist_ok=True)
        except OSError as e:
            return Response(
                data={"status": {"code": 1, "message": f"Failed to create directory: {str(e)}"}, "data": {}},
                status=status.HTTP_200_OK
            )

        try:
            with transaction.atomic():
                collection = Collection.objects.create(
                    name=name,
                    path=collection_path,
                    project=project
                )
        except IntegrityError:
            return Response(
                data={"status": {"code": 1, "message": "conflict on unique fields"}, "data": {}},
                status=status.HTTP_200_OK
            )

        devices = Device.objects.all()
        flash_setting = FlashSetting.get_settings()
        trigger(flash_setting.delay)
        all_photos = get_photo_list(devices)

        for photo in all_photos:
            print(photo)
            image = get_device_photo(photo.get("download_url"))
            photo_name = photo.get("filename")

            file_path = os.path.join(collection.path, photo_name)

            with open(file_path, 'wb') as f:
                f.write(image.content)

            File.objects.create(
                name=photo_name,
                path=file_path,
                size=len(image.content),
                collection=collection
            )

        serializer = CollectionSerializer(collection)

        return Response(
            data={"status": {"code": 0, "message": "success"}, "data": serializer.data},
            status=status.HTTP_200_OK
        )