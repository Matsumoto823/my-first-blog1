from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, ContinuationModel
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import timedelta

# Create your views here.
def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request. POST or None)
    if create_theme_form.is_valid():
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        messages.success(request, '項目を追加しました。')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/create_theme.html', context={
          'create_theme_form':create_theme_form,
        }
    )
    
def list_themes(request):
    themes = Themes.objects.all()
    return render(
        request, 'boards/list_themes.html', context={
            'themes': themes    
        }
    )
    
def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, '捨てるモノを更新しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )    
    
def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid():
        theme.delete()
        messages.success(request, '捨てるモノの登録を削除しました')
        return redirect('boards:list_themes')
    return render(
        request, 'boards/delete_theme.html', context={
            'delete_theme_form': delete_theme_form,
        }
    )
    
def update_check(request):
    if request.method == 'POST':
        # ユーザーに関連するテーマを取得
        themes = Themes.objects.filter(user=request.user)

        for theme in themes:
            # フォームから送信されたチェックボックスの状態を取得
            is_checked = f'checked_{theme.id}' in request.POST
            theme.is_checked = is_checked  # チェック状態を更新
            theme.save()  # チェック状態を保存

        # チェック状態を保存後、テーマ一覧画面にリダイレクト
        return redirect('boards:list_themes')
      


def update_check(request):
    if request.method == 'POST':
        themes = Themes.objects.filter(user=request.user)

        for theme in themes:
            is_checked = f'checked_{theme.id}' in request.POST
            theme.is_checked = is_checked  # チェック状態を更新
            
            # チェックが付けられた場合、checked_atを更新
            if is_checked:
                theme.checked_at = timezone.now()  # 現在の日時を設定
            else:
                theme.checked_at = None  # チェックが外れた場合はNoneに設定

            theme.save()  # チェック状態とchecked_atを保存

        return redirect('boards:list_themes')


def calculate_continuous_days(theme):
    if theme.is_checked and theme.checked_at:
        # チェックされた日からの継続日数を計算
        return (timezone.now().date() - theme.checked_at.date()).days + 1  # 今日も含める
    return 0


@login_required
def list_themes(request):
    # 表示モードの取得（デフォルトはすべてのデータを表示）
    show_user_only = request.GET.get('show_user_only', 'false') == 'true'

    # ログインしているユーザーのデータを取得
    user_themes = Themes.objects.filter(user=request.user)

    if show_user_only:
        # ユーザー自身のテーマのみを表示
        all_themes = user_themes
    else:
        # すべてのテーマを表示
        all_themes = Themes.objects.all()

    # 各テーマの継続日数を計算
    for theme in user_themes:
        theme.continuous_days = calculate_continuous_days(theme)

    context = {
        'user_themes': user_themes,
        'all_themes': all_themes,
        'show_user_only': show_user_only,  # 現在の表示モードをテンプレートに渡す
    }
    
    return render(request, 'boards/list_themes.html', context)
