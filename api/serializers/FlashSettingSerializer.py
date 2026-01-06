from rest_framework import serializers
from api.models import FlashSetting


class FlashSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashSetting
        fields = '__all__'


