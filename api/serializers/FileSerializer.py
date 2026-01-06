from rest_framework import serializers
from api.models import File

class FileSerializer(serializers.ModelSerializer):
    collection_name = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = '__all__'

    def get_collection_name(self, obj):
        return obj.collection.name

    def get_project_name(self, obj):
        return obj.collection.project.name
