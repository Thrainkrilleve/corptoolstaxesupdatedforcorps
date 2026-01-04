from django.shortcuts import render
from django.http import Http404

from . import __version__
from .models import CorpTaxConfiguration

"""
    add views?
"""


def react_bootstrap(request):
    data = []
    try:
        ct = CorpTaxConfiguration.objects.get(pk=1)
        ct.send_invoices()
    except CorpTaxConfiguration.DoesNotExist:
        raise Http404("Tax configuration not found")
    return render(request, 'taxtools/react_base.html', context={"data": "\n".join(data)})
