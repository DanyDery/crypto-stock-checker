from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import FutureValueForm


def get_data(request):
    if request.method == 'POST':
        form = FutureValueForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/result/')
    else:
        form = FutureValueForm
    return render(request, 'fv.html', {'form': form})

# def home(request):
# return HttpResponse('<h3>Compute the future value</h3>'
#                     '<h3>Compute the interest portion of a payment</h3>'
#                     '<h3>Return the Internal Rate of Return (IRR)</h3>'
#                     '<h3>Modified internal rate of return</h3>'
#                     '<h3>Compute the number of periodic payments</h3>'
#                     '<h3>Returns the NPV (Net Present Value) of a cash flow series</h3>'
#                     '<h3>Compute the payment against loan principal plus interest</h3>'
#                     '<h3>Compute the payment against loan principal</h3>'
#                     '<h3>Compute the rate of interest per period</h3>'
#                     '<h3>Compute the present value</h3>'
#                     )
