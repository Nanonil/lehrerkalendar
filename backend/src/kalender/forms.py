from django import forms
from django.db.utils import OperationalError
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
    try:
        classes = Schoolclass.objects.all()

        CHOICES = []
        i = 1
        for sc in classes:
            CHOICES.append((i, sc.ClassName))
            i += 1

        Klasse = forms.ChoiceField(choices=CHOICES)  # initial=classId
    except OperationalError:
        pass