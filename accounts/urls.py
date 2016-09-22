from django.conf.urls import include, url


urlpatterns = [
    # Examples:
    # url(r'^$', 'loginproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'login/$', 'accounts.views.login', name='login'),
    url(r'register/$', 'accounts.views.register', name='register'),
    url(r'logout/$', 'accounts.views.logout', name='logout'),
    url(r'changepassword/$', 'accounts.views.changepassword', name='changepassword'),
    url(r'userlist/$', 'accounts.views.userlist', name='userlist'),
    url(r'addstu/$', 'accounts.views.addstu', name='addstu'),
    url(r'addtea/$', 'accounts.views.addtea', name='addtea'),
    url(r'tealist/$', 'accounts.views.tealist', name='tealist'),
    url(r'stulist/$', 'accounts.views.stulist', name='stulist'),
    url(r'impstu/$', 'accounts.views.impstu', name='impstu'),
    url(r'download/(?P<pp>[A-Za-z]+)/$', 'qq.views.downtemplate', name='downtemplate'),
]
