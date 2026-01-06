from django.db import models
from django.core.exceptions import ValidationError


class CameraSetting(models.Model):
    ISO_SPEED_CHOICES = [
        ('Auto', 'Auto'),
        ('100', '100'),
        ('200', '200'),
        ('400', '400'),
        ('800', '800'),
        ('1600', '1600'),
        ('3200', '3200'),
        ('6400', '6400'),
    ]

    SHUTTER_SPEED_CHOICES = [
        ('bulb', 'bulb'),
        ('30', '30'),
        ('25', '25'),
        ('20', '20'),
        ('15', '15'),
        ('13', '13'),
        ('10.3', '10.3'),
        ('8', '8'),
        ('6.3', '6.3'),
        ('5', '5'),
        ('4', '4'),
        ('3.2', '3.2'),
        ('2.5', '2.5'),
        ('2', '2'),
        ('1.6', '1.6'),
        ('1.3', '1.3'),
        ('1', '1'),
        ('0.8', '0.8'),
        ('0.6', '0.6'),
        ('0.5', '0.5'),
        ('0.4', '0.4'),
        ('0.3', '0.3'),
        ('1/4', '1/4'),
        ('1/5', '1/5'),
        ('1/6', '1/6'),
        ('1/8', '1/8'),
        ('1/10', '1/10'),
        ('1/13', '1/13'),
        ('1/15', '1/15'),
        ('1/20', '1/20'),
        ('1/25', '1/25'),
        ('1/30', '1/30'),
        ('1/40', '1/40'),
        ('1/50', '1/50'),
        ('1/60', '1/60'),
        ('1/80', '1/80'),
        ('1/100', '1/100'),
        ('1/125', '1/125'),
        ('1/160', '1/160'),
        ('1/200', '1/200'),
        ('1/250', '1/250'),
        ('1/320', '1/320'),
        ('1/400', '1/400'),
        ('1/500', '1/500'),
        ('1/640', '1/640'),
        ('1/800', '1/800'),
        ('1/1000', '1/1000'),
        ('1/1250', '1/1250'),
        ('1/1600', '1/1600'),
        ('1/2000', '1/2000'),
        ('1/2500', '1/2500'),
        ('1/3200', '1/3200'),
        ('1/4000', '1/4000'),
    ]

    APERTURE_CHOICES = [
        ('4', '4'),
        ('4.5', '4.5'),
        ('5', '5'),
        ('5.6', '5.6'),
        ('6.3', '6.3'),
        ('7.1', '7.1'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('13', '13'),
        ('14', '14'),
        ('16', '16'),
        ('18', '18'),
        ('20', '20'),
        ('22', '22'),
        ('25', '25'),
    ]

    WHITE_BALANCE_CHOICES = [
        ('Auto', 'Auto'),
        ('Daylight', 'Daylight'),
        ('Shadow', 'Shadow'),
        ('Cloudy', 'Cloudy'),
        ('Tungsten', 'Tungsten'),
        ('Fluorescent', 'Fluorescent'),
        ('Flash', 'Flash'),
        ('Manual', 'Manual'),
    ]

    IMAGE_FORMAT_CHOICES = [
        ('L', 'L'),
        ('cL', 'cL'),
        ('M', 'M'),
        ('cM', 'cM'),
        ('S1', 'S1'),
        ('cS1', 'cS1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
        ('RAW + L', 'RAW + L'),
        ('RAW', 'RAW'),
    ]

    DRIVE_MODE_CHOICES = [
        ('Single', 'Single'),
        ('Continuous', 'Continuous'),
        ('Timer 10 sec', 'Timer 10 sec'),
        ('Timer 2 sec', 'Timer 2 sec'),
        ('Continuous timer', 'Continuous timer'),
    ]

    METERING_MODE_CHOICES = [
        ('Evaluative', 'Evaluative'),
        ('Partial', 'Partial'),
        ('Center-weighted average', 'Center-weighted average'),
    ]

    PICTURE_STYLE_CHOICES = [
        ('Auto', 'Auto'),
        ('Standard', 'Standard'),
        ('Portrait', 'Portrait'),
        ('Landscape', 'Landscape'),
        ('Neutral', 'Neutral'),
        ('Faithful', 'Faithful'),
        ('Monochrome', 'Monochrome'),
        ('User defined 1', 'User defined 1'),
        ('User defined 2', 'User defined 2'),
        ('User defined 3', 'User defined 3'),
    ]

    iso_speed = models.CharField(
        max_length=10,
        choices=ISO_SPEED_CHOICES,
        default='Auto'
    )

    shutter_speed = models.CharField(
        max_length=10,
        choices=SHUTTER_SPEED_CHOICES,
        default='1/60'
    )

    aperture = models.CharField(
        max_length=5,
        choices=APERTURE_CHOICES,
        default='8'
    )

    white_balance = models.CharField(
        max_length=20,
        choices=WHITE_BALANCE_CHOICES,
        default='Auto'
    )

    image_format = models.CharField(
        max_length=10,
        choices=IMAGE_FORMAT_CHOICES,
        default='L'
    )

    drive_mode = models.CharField(
        max_length=20,
        choices=DRIVE_MODE_CHOICES,
        default='Single'
    )

    metering_mode = models.CharField(
        max_length=30,
        choices=METERING_MODE_CHOICES,
        default='Evaluative'
    )

    picture_style = models.CharField(
        max_length=20,
        choices=PICTURE_STYLE_CHOICES,
        default='Auto'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Camera Setting"
        verbose_name_plural = "Camera Settings"

    def save(self, *args, **kwargs):
        if not self.pk and CameraSetting.objects.exists():
            raise ValidationError("Only one CameraSetting instance is allowed")
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Singleton instance'ı getir veya oluştur"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def __str__(self):
        return f"Camera Settings (ISO: {self.iso_speed}, Shutter: {self.shutter_speed}, Aperture: {self.aperture})"