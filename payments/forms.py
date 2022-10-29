from django import forms


class FutureValueForm(forms.Form):
    rate = forms.CharField(label='Rate of interest', max_length=3)
    nper = forms.CharField(label='Number of compounding periods', max_length=3)
    pmt = forms.CharField(label='Payment', max_length=10)
    pv = forms.CharField(label='Present value', max_length=10)
