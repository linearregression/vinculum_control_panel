from django.shortcuts import render

from django.views.generic import TemplateView
from django.http.response import HttpResponsePermanentRedirect

# Create your views here.
from vinculum.models import Vinculum


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['vinculums'] = Vinculum.objects.filter(owner=self.request.user)
        return context