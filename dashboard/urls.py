from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from views import DashboardView


urlpatterns = [
    url(r"^$", DashboardView.as_view(), name="dashboard"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
