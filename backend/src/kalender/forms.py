from django import forms
from bootstrap_datepicker_plus import DatePickerInput


class DatepickerForm(forms.Form):
    date = forms.DateField(
        widget=DatePickerInput(format='%d/%m/%Y')
    )
