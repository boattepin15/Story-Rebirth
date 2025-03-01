from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline, TabularInline
from django.utils.html import mark_safe


from novels.models import (
    Novels,
    Category,
    Tags,
    ChapterNovels,
    UpdateDay
)




@admin.register(Tags)
class CategoryAdmin(ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass

@admin.register(UpdateDay)
class UpdateDayAdmin(ModelAdmin):
    list_display = ('day',)
    search_fields = ('day',)

class ChapterNovelInline(StackedInline):
    model = ChapterNovels
    tab = True
    extra = 0
    


@admin.register(ChapterNovels)
class ChapterNovelsAdmin(ModelAdmin):
    """จัดการตอนนิยายในระบบ"""
    fieldsets = (
        (None, {
            "fields": (
                'order',
                'title',
                'content',
                'is_locked',
                ('like', 'viewer'),
                'created_at',  
                'updated_at', 
            ),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')  # ฟิลด์ที่ไม่สามารถแก้ไขได้
    list_display = ('title', 'novel', 'order', 'is_locked', 'viewer', 'like', 'created_at', 'updated_at')
    list_editable = ('is_locked', 'order')  # แก้ไขสถานะล็อกและลำดับตอนจากหน้า List View
    search_fields = ('title', 'novel__title')  # เพิ่มช่องค้นหาตามชื่อตอนและนิยาย
    list_filter = ('is_locked', 'created_at', 'updated_at')  # เพิ่มตัวกรองสำหรับสถานะและวันที่สร้าง
    empty_value_display = '-ไม่มีข้อมูล-'
    
@admin.register(Novels)
class NovelsAdmin(ModelAdmin):
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
    inlines = [ChapterNovelInline]  
    list_display = ('display_image','title', 'author', 'status', 'price', 'viewer', 'created_at')  
    list_filter = ('status', 'created_at', 'publish_at')  
    search_fields = ('title', 'author')

    def display_image(self, obj):
        """แสดงรูปภาพใน List Display"""
        if obj.image:  # ตรวจสอบว่ามีรูปภาพหรือไม่
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="border-radius: 5px;" />')
        return "No Image"