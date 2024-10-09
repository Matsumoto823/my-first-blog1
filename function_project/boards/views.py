from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes
from django.http import Http404

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