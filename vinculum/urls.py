from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns


from views import VinculumDetail, VinculumList

urlpatterns = [
    url(r"^$", VinculumList.as_view()),
    url(r"^(?P<pk>[0-9]+)$", VinculumDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)