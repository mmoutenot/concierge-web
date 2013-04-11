from django.conf.urls import patterns, url
urlpatterns = patterns('goto.views',
    url(r'^pickgotos/', 'pickgotos',
        name='pickgotos'),
    url(r'^savegotos/', 'savegotos',
        name='savegotos'),
)
