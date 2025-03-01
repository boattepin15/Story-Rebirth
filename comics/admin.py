from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline, TabularInline
from django.utils.html import mark_safe

from comics.models import Comics


@admin.register(Comics)
class ComicsAdmin(ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ('image'),
                ('title'),
                ('author'),
                ('copyright'),
                ('category'),
                ('tags'),
                ('status'),
                ('price', 'like', 'viewer'),
                ('description'),
                ('publish_at', 'update_days'),
                ('created_at', 'updated_at'),
            ),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'slug')  
    list_display = ('display_image','title', 'author', 'status', 'price', 'viewer', 'created_at')  
    list_filter = ('status', 'created_at', 'publish_at')  
    search_fields = ('title', 'author')

    def display_image(self, obj):
        """แสดงรูปภาพใน List Display"""
        if obj.image:  # ตรวจสอบว่ามีรูปภาพหรือไม่
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="border-radius: 5px;" />')
        return "No Image"