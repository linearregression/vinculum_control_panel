from django.shortcuts import render

from django.views.generic import View
from django.http.response import HttpResponsePermanentRedirect

# Create your views here.

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        if request.user.is_authenticated() is False:
            return HttpResponsePermanentRedirect("/")
        else:
            return render(request=request, template_name="dashboard.html")