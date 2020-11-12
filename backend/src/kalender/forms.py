from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from datetime import date as dateTime
from .models import *

defaultDate = None

class DatepickerForm(forms.Form):
    if defaultDate is None:
        defaultDate = dateTime.today()
    date = forms.DateField(
        widget=DatePickerInput(format='%d/%m/%Y', attrs={'value': defaultDate})
    )

class ClassForm(forms.Form):
    classes = Schoolclass.objects.all()
    

    # CHOICES = (
    #         (1, 'FIA83'),
    #         (2, 'FIA84'),
    #         (3, 'FIA85')
    # )
    CHOICES = []
    i = 1
    for sc in classes:
        CHOICES.append((i, sc.ClassName))
        i += 1
        
    Klasse = forms.ChoiceField(choices=CHOICES) #initial=classId