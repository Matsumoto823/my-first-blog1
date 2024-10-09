from django import forms
from .models import Themes


class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='捨てるモノ')
    
        
    class Meta:
        model = Themes
        fields  = ('title',)    
        
class DeleteThemeForm(forms.ModelForm):
  
    class Meta:
        model = Themes
        fields = [] 