from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'qqqq.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', 'qq.views.home', name='home'),
    url(r'qlist/$', 'qq.views.qlist', name='qlist'),
    url(r'upfiles/$', 'qq.views.upfiles', name='upfiles'),
    url(r'preview/(?P<pp>[0-9]+)/$', 'qq.views.preview', name='preview'),
    url(r'qview/(?P<pp>[0-9]+)/$', 'qq.views.qview', name='qview'),
    url(r'qstore/(?P<pp>[0-9]+)/$', 'qq.views.qstore', name='qstore'),
    url(r'qdelete/(?P<pp>[0-9]+)/$', 'qq.views.qdelete', name='qdelete'),
    url(r'q_submit/(?P<pp>[0-9]+)/$', 'qq.views.q_submit', name='q_submit'),
    url(r'q_result/(?P<pp>[0-9]+)/$', 'qq.views.q_result', name='q_result'),
    url(r'rlist/$', 'qq.views.rlist', name='rlist'),
    url(r'rdelete/(?P<pp>[0-9]+)/$', 'qq.views.rdelete', name='rdelete'),
    #url(r'download/(?P<pp>[A-Za-z]+)/$', 'qq.views.downtemplate', name='downtemplate'),#account里面已经有了这一条了
]
