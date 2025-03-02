from django import forms
from .models import Timers

class PomodoroForm(forms.ModelForm):
  

    class Meta:
        model = Timers
        fields = ['band_name','minutes','item1','item2','item3',]
        TASK_CHOICES = [
            ('', '選択してください'),
            ('よんく', 'よんく'),
            ('あお', 'あお'),
            ('キャロ', 'キャロ'),
            ('ジョンレノ', 'ジョンレノ'),
            ('つね', 'つね'),
            ('やお', 'やお'),
            ('いぶき', 'いぶき'),
            ('そら', 'そら'),
            ('茈', '茈'),
        ]
        labels = {
            'band_name': 'バンド名',
            'minutes': '時間(分)',
            'item1': '管理１',
            'item2': '管理２',
            'item3': '管理３',
        }
        widgets = {
            'band_name': forms.TextInput(attrs={'required': 'required'}),
            'minutes': forms.NumberInput(attrs={'required': 'required'}),
            'item1': forms.Select(choices=TASK_CHOICES, attrs={'required': 'required'}),
            'item2': forms.Select(choices=TASK_CHOICES, attrs={'required': 'required'}),
            'item3': forms.Select(choices=TASK_CHOICES, attrs={'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        minutes = cleaned_data.get('minutes', 0)

        if minutes < 0:
            raise forms.ValidationError("Minutes must be non-negative.")

        return cleaned_data