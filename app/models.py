from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name='ชื่อหมวดหมู่', max_length=255)
    description = models.CharField(verbose_name='คำอธิบายเพิ่มเติม', max_length=255)
    update_ad = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'
        verbose_name = 'หมวดหมู่'
        verbose_name_plural = 'หมวดหมู่'

class Tags(models.Model):
    name = models.CharField(verbose_name='ชื่อแท็ก', max_length=255)
    description = models.CharField(verbose_name='คำอธิบายเพิ่มเติม', max_length=255)
    update_ad = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.name

    class Meta:
        db_table = 'Tags'
        verbose_name = 'แท็ก'
        verbose_name_plural = 'แท็ก'

class UpdateDay(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'วันจันทร์'),
        ('tue', 'วันอังคาร'),
        ('wed', 'วันพุธ'),
        ('thu', 'วันพฤหัสบดี'),
        ('fri', 'วันศุกร์'),
        ('sat', 'วันเสาร์'),
        ('sun', 'วันอาทิตย์'),
    ]
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return self.get_day_display()

    class Meta:
        db_table = 'update_day'
        verbose_name = 'ตารางอัปเดต'
        verbose_name_plural = 'ตารางอัปเดต'
        ordering = ['day']
