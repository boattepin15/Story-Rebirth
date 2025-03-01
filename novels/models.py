from django.db import models
from django.utils import timezone
from datetime import datetime
from autoslug import AutoSlugField # type: ignore
from django_ckeditor_5.fields import CKEditor5Field # type: ignore
import uuid
import os
from app.models import (
    Category,
    Tags,
    UpdateDay
)

def content_covers(instance, filename):
    ext = os.path.splitext(filename)[1]
    unique_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'{unique_id}{uuid.uuid4()}{ext}'
    return os.path.join('uploads','images', 'content_covers', f'{unique_id}', filename)


class BaseContent(models.Model):
    COPYRIGHT_CHOICES = [
        ('มีลิขสิทธิ์', 'มีลิขสิทธิ์'),
        ('ยังไม่มีลิขสิทธิ์', 'ยังไม่มีลิขสิทธิ์'),
    ]

    STATUS_CHOICES = [
        ('จบแล้ว', 'จบแล้ว'),
        ('ยังไม่จบ', 'ยังไม่จบ'),
        ('หยุดชั่วคราว', 'หยุดชั่วคราว'),
        ('กำลังฉาย', 'กำลังฉาย'),
    ]
    
    title = models.CharField(verbose_name="ชื่อเรื่อง", max_length=255) 
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, verbose_name="Slug")
    author = models.CharField(verbose_name="ผู้แต่ง", max_length=255)
    description = models.TextField(verbose_name="รายละเอียด")
    image = models.ImageField(verbose_name='รูปภาพปก', upload_to=content_covers)
    category = models.ManyToManyField(
        Category,
        verbose_name='หมวดหมู่'
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='แท็ก'
    )
    copyright = models.CharField(verbose_name='ลิขสิทธิ์',
                                max_length=255,
                                choices=COPYRIGHT_CHOICES,
                                default='ยังไม่มีลิขสิทธิ์'
                                )
    status = models.CharField(verbose_name='สถาณะเรื่องนี้',
                              max_length=255,
                              choices=STATUS_CHOICES, default='กำลังฉาย')
    price = models.PositiveIntegerField(verbose_name='ราคาขายต่อตอน')
    like = models.PositiveIntegerField(verbose_name='จำการกดถูกใจ', default=0)
    viewer = models.PositiveIntegerField(verbose_name='จำนวนคนอ่าน', default=0)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateField(verbose_name="วันเวลาเปิดให้อ่าน")

    @property
    def popularity_score(self):
        """คำนวณคะแนนความนิยมโดยรวมโดยใช้จำนวนผู้ชมและจำนวนไลค์"""
        # น้ำหนักที่ให้กับไลค์มากกว่าวิว เพราะแสดงถึงการมีส่วนร่วมที่มากกว่า
        return (self.viewer * 1) + (self.like * 3)
    
    def is_published(self):
        return self.publish_at and self.publish_at <= timezone.now()
    
    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['viewer']),
            models.Index(fields=['like']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['publish_at']),

        ]


class Novels(BaseContent):
    update_days = models.ManyToManyField(UpdateDay, verbose_name="วันที่อัปเดต", blank=True)
    class Meta:
        db_table = 'novels'
        verbose_name = 'นิยาย'
        verbose_name_plural = 'นิยาย'


class ChapterNovels(models.Model):
    novel = models.ForeignKey(
        Novels,
        on_delete=models.CASCADE,
        related_name='chapters',
        verbose_name='นิยาย'
    )
    title = models.CharField(verbose_name="ชื่อตอน", max_length=255) 
    content = CKEditor5Field('content', config_name='extends')
    order = models.PositiveIntegerField(verbose_name="ลำดับตอน") 
    is_locked = models.BooleanField(verbose_name="ล็อกตอนนี้หรือไม่", default=True)
    like = models.PositiveIntegerField(verbose_name='จำการกดถูกใจ', default=0)
    viewer = models.PositiveIntegerField(verbose_name='จำนวนคนอ่าน', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def popularity_score(self):
        return (self.viewer *1) + (self.like *3)
    
    class Meta:
        db_table = 'chapters_novel'
        verbose_name = 'ตอน'
        verbose_name_plural = 'ตอน'
        ordering = ['order']

