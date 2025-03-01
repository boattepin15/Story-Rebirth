from comics.models import Comics
from novels.models import Novels
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, FloatField


class HomeView(TemplateView):
    template_name = 'app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dictionary of day abbreviations
        days = {
            'mon': 'Monday',
            'tue': 'Tuesday', 
            'wed': 'Wednesday',
            'thu': 'Thursday',
            'fri': 'Friday',
            'sat': 'Saturday',
            'sun': 'Sunday'
        }
        
        # Get comics and novels organized by update days
        context['comics_by_day'] = {
            day_abbr: Comics.objects.filter(update_days__day=day_abbr).distinct()
            for day_abbr in days.keys()
        }
        # Get nover by update days
        context['novels_by_day'] = {
            day_abbr: Novels.objects.filter(update_days__day=day_abbr).distinct()
            for day_abbr in days.keys()
        }
        
        # Get the current day to make that tab active by default
        current_day = timezone.now().strftime('%a').lower()
        context['current_day'] = current_day

        # Get Novel and comics last update
        # context['latest_comics'] = Comics.objects.filter(status='active').order_by('-updated_at')[:6]
        # context['latest_novels'] = Novels.objects.filter(status='active').order_by('-updated_at')[:6]
        #mockup
        context['latest_comics'] = Comics.objects.all()
        context['latest_novels'] = Novels.objects.all()

        context['popular_comics'] = Comics.objects.filter(
            publish_at__lte=timezone.now().date()  # ตรวจสอบว่าได้ตีพิมพ์แล้ว
        ).annotate(
            popularity=ExpressionWrapper(
                (F('viewer') * 1.0) + (F('like') * 3.0),  # ไลค์มีน้ำหนัก 3 เท่าของวิว
                output_field=FloatField()
            )
        ).prefetch_related('category').order_by('-popularity')[:12]  # เพิ่มจำนวนเป็น 12 เพื่อแสดงในหน้าหลัก
        
        # ปรับปรุงการดึงนิยายยอดนิยม
        context['popular_novels'] = Novels.objects.filter(
            publish_at__lte=timezone.now().date()  # ตรวจสอบว่าได้ตีพิมพ์แล้ว
        ).annotate(
            popularity=ExpressionWrapper(
                (F('viewer') * 1.0) + (F('like') * 3.0),  # ไลค์มีน้ำหนัก 3 เท่าของวิว
                output_field=FloatField()
            )
        ).prefetch_related('category').order_by('-popularity')[:12]  # เพิ่มจำนวนเป็น 12 เพื่อแสดงในหน้าหลัก

        
        # อันดับนิยายตามยอดไลค์
        # ลองดึงข้อมูลใน 7 วันล่าสุดก่อน
        recent_liked_novels = Novels.objects.filter(
            publish_at__lte=timezone.now().date(),
            updated_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-like')[:5]

        # ถ้าไม่มีข้อมูลในช่วง 7 วัน ให้ดึงข้อมูลทั้งหมดแทน
        if recent_liked_novels.count() == 0:
            context['top_liked_novels'] = Novels.objects.all().order_by('-like')[:5]
        else:
            context['top_liked_novels'] = recent_liked_novels

        # อันดับนิยายตามยอดวิว
        recent_viewed_novels = Novels.objects.filter(
            publish_at__lte=timezone.now().date(),
            updated_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-viewer')[:5]

        if recent_viewed_novels.count() == 0:
            context['top_viewed_novels'] = Novels.objects.all().order_by('-viewer')[:5]
        else:
            context['top_viewed_novels'] = recent_viewed_novels

        # อันดับการ์ตูนตามยอดไลค์
        recent_liked_comics = Comics.objects.filter(
            publish_at__lte=timezone.now().date(),
            updated_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-like')[:5]

        if recent_liked_comics.count() == 0:
            context['top_liked_comics'] = Comics.objects.all().order_by('-like')[:5]
        else:
            context['top_liked_comics'] = recent_liked_comics

        # อันดับการ์ตูนตามยอดวิว
        recent_viewed_comics = Comics.objects.filter(
            publish_at__lte=timezone.now().date(),
            updated_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-viewer')[:5]

        if recent_viewed_comics.count() == 0:
            context['top_viewed_comics'] = Comics.objects.all().order_by('-viewer')[:5]
        else:
            context['top_viewed_comics'] = recent_viewed_comics


        # อันดับนิยายตามยอดไลค์
        recent_liked_novels = Novels.objects.filter(
            publish_at__lte=timezone.now().date(),
            updated_at__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-like')[:5]

        if recent_liked_novels.count() == 0:
            context['top_liked_novels'] = Novels.objects.all().order_by('-like')[:5]
            context['liked_novels_time_period'] = 'all'  # ระบุว่าเป็นข้อมูลทั้งหมด
        else:
            context['top_liked_novels'] = recent_liked_novels
            context['liked_novels_time_period'] = '7days'  # ระบุว่าเป็นข้อมูล 7 วัน

        return context
