from django.conf.urls.defaults import *
from apps.api import views

urlpatterns = patterns('', url(r'^new_game', views.new_game, name='api-new-game'),
                       url(r'^submit_player_move', views.submit_player_move, name='api-submit-player-move'),
                       url(r'^submit_bot_move', views.submit_bot_move, name='api-submit-bot-move'))
