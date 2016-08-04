from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    # the pinax front page

    url(r"^admin/", include(admin.site.urls)),
    url(r"^vinculums/", include("vinculum.urls")),
    # django rest frameowkr endpoint for vinculums

    url(r"^dashboard/", include("dashboard.urls")),
    # single template view of a dashboard, but we include other things such as a list of vinculums

    url(r"^account/", include("account.urls")),
    # pinax accounts app

    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
