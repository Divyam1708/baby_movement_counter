from django import forms
from .models import Movement
from django.utils import timezone
class CreateMovement(forms.ModelForm):
    class Meta:
        model=Movement
        fields=[]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False


class CreateMovementUnsynchronisedForm(forms.ModelForm):
    class Meta:
        model=Movement
        fields=['movement_time']
        
        widgets = {
            'movement_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            )
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movement_time'].initial=timezone.now()
        
        
class GoToDateForm(forms.Form):
    day=forms.ChoiceField(
        choices=[(x,f'{x:02d}') for x in range(1,32)],
        initial=timezone.localdate().day
    )
    month=forms.ChoiceField(
        choices=[(x,f'{x:02d}') for x in range(1,13)],
        initial=timezone.localdate().month
    )
    year=forms.ChoiceField(
        choices=[(x,f'{x:02d}') for x in range(2026,2030)],
        initial=timezone.localdate().year
    )
    