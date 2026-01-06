from rest_framework import serializers
from api.models import CameraSetting


class CameraSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraSetting
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['choices'] = {
            'iso_speed': [choice[0] for choice in CameraSetting.ISO_SPEED_CHOICES],
            'shutter_speed': [choice[0] for choice in CameraSetting.SHUTTER_SPEED_CHOICES],
            'aperture': [choice[0] for choice in CameraSetting.APERTURE_CHOICES],
            'white_balance': [choice[0] for choice in CameraSetting.WHITE_BALANCE_CHOICES],
            'image_format': [choice[0] for choice in CameraSetting.IMAGE_FORMAT_CHOICES],
            'drive_mode': [choice[0] for choice in CameraSetting.DRIVE_MODE_CHOICES],
            'metering_mode': [choice[0] for choice in CameraSetting.METERING_MODE_CHOICES],
            'picture_style': [choice[0] for choice in CameraSetting.PICTURE_STYLE_CHOICES],
        }

        return data
