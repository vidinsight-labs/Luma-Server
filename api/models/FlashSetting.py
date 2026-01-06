from django.db import models
from django.core.exceptions import ValidationError


class FlashSetting(models.Model):
    delay = models.IntegerField(
        default=0,
        help_text="Flash delay in milliseconds"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Flash Setting"
        verbose_name_plural = "Flash Settings"

    def save(self, *args, **kwargs):
        if not self.pk and FlashSetting.objects.exists():
            raise ValidationError("Only one FlashSetting instance is allowed")
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Singleton instance'ı getir veya oluştur"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def __str__(self):
        return f"Flash Setting (Delay: {self.delay}ms)"