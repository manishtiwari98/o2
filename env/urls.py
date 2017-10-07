
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^tree/$',views.tree_loc,name='tree_loc'),
    url(r'^leaderboard/$',views.leaderboard,name='leaderboard'),
    url(r'^news/$',views.news,name='news')
]
