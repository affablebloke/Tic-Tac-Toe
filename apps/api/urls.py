from django.conf.urls.defaults import *
from apps.api import views

urlpatterns = patterns('', url(r'^game', views.game, name='api-game'),
                       url(r'^submit_move', views.submit_move, name='api-submit-move'),
                       url(r'^check_for_win', views.check_for_win, name='api-check-for-win'),)
