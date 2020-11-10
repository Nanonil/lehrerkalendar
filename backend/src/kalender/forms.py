from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class DateInput(forms.DateInput):
    input_type = 'date'

class DatepickerForm(forms.Form):
    date = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "dd/mm/yyyy",
                "autoclose": True
            }
        )
    )