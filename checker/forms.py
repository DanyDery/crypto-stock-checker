from django import forms


class TickerForm(forms.Form):
    ticker = forms.CharField(label='', max_length=5, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Search for ticker'
        }
    ))
