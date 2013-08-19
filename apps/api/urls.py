from django.conf.urls.defaults import *
from apps.api import views

urlpatterns = patterns('', url(r'^new_game', views.newgame, name='api-new-game')
)
