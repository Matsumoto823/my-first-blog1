from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class ThemesManager(models.Manager):
    def fetch_all_themes(self):
        return self.order_by('id').all()

class Themes(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)  # チェックボックス用のフィールドを追加
    created_at = models.DateTimeField(auto_now_add=True)  # データ追加日時を記録するフィールド
    checked_at = models.DateTimeField(null=True, blank=True)  # チェックを付けた日
    
    objects = ThemesManager()

    class Meta:
        db_table = 'themes'

class ContinuationModel(models.Model):
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_user_continuous_days_count(user_id):
        today = timezone.now().date()
        # 特定のユーザーに関連するすべてのテーマのデータを取得
        data_dates = ContinuationModel.objects.filter(theme__user_id=user_id).values_list('created_at', flat=True)
        data_dates = sorted([date.date() for date in data_dates], reverse=True)

        # 連続している日数をカウント
        continuous_days = 0
        for i, date in enumerate(data_dates):
            if date == today - timedelta(days=i):
                continuous_days += 1
            else:
                break

        return continuous_days
