from rest_framework import serializers
from api.models import Collection

class CollectionSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'

    def get_project_name(self, obj):
        return obj.project.name