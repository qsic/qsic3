from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect


def index_redirect(request):
    return HttpResponseRedirect(reverse('qsic:up_next'))
