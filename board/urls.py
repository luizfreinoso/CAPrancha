from django.conf.urls import url
from board import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pg>\d+)/$', views.NextView, name='pagination')
]