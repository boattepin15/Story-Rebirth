from django.db import models

# Create your models here.
from novels.models import (
    BaseContent,
    UpdateDay
)


class Comics(BaseContent):
    update_days = models.ManyToManyField(UpdateDay, verbose_name="วันที่อัปเดต", blank=True)
    class Meta:
        db_table = 'comics'
        verbose_name = 'การ์ตูน'
        verbose_name_plural = 'การ์ตูน'


