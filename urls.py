from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^api/',              include('apps.api.urls')),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'game.html'}),
)
