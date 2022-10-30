from django import forms


class FutureValueForm(forms.Form):
    rate = forms.DecimalField(label='Rate of interest', max_value=0.001, min_value=0.999, decimal_places=3)
    nper = forms.IntegerField(label='Number of compounding periods', max_value=100, min_value=1)
    pmt = forms.IntegerField(label='Regular payment')
    pv = forms.IntegerField(label='Present contribution')
