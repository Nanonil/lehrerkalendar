from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from datetime import date as dateTime

defaultDate = None

class DatepickerForm(forms.Form):
    if defaultDate is None:
        defaultDate = dateTime.today()
    date = forms.DateField(
        #'12/12/2020'
        widget=DatePickerInput(format='%d/%m/%Y', attrs={'value': defaultDate})
    )