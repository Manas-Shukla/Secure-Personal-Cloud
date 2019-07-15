from django.conf.urls import url
from django.views.generic import ListView ,TemplateView
from . import views

urlpatterns = [
    url('^sign_up',views.sign_up,name='sign_up'),
    url('^reset_password',views.reset_password,name='reset_password'),
    url('^login',views.login,name='login'),
    url('^logout',views.logout,name='logout'),
    url('^homepage/root=(.+)',views.homepage,name='homepage'),

]
#more ideas :
# deactivate account
