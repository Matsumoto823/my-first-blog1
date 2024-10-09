from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class ThemesManager(models.Manager):
    
    def fetch_all_themes(self):
        return self.order_by('id').all()  


class Themes(models.Model):
  
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    
    objects = ThemesManager() 
    
    class Meta:
        db_table = 'themes'
        
   
class Themes(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # auth.Userの代わりにAUTH_USER_MODELを使用
    is_checked = models.BooleanField(default=False)   # チェックボックス用のフィールドを追加
    


class ContinuationModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # データが追加された日

    @staticmethod
    def get_continuous_days_count():
        # 最新の追加日から今日までの連続追加日数をカウント
        today = timezone.now().date()
        data_dates = ContinuationModel.objects.values_list('created_at', flat=True)
        data_dates = sorted([date.date() for date in data_dates], reverse=True)

        # 連続している日数をカウント
        continuous_days = 0
        for i, date in enumerate(data_dates):
            if date == today - timedelta(days=i):
                continuous_days += 1
            else:
                break  # 連続しなくなったら終了

        return continuous_days
