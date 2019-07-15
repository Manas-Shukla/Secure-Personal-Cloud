from django.conf.urls import url
from django.views.generic import ListView ,TemplateView
from . import views

urlpatterns = [
    url('^check_server',views.check_server,name='check_server'),
    url('^sign_up',views.sign_up,name='sign_up'),
    url('^request_for_sync',views.request_for_sync,name='request_for_sync'),
    url('^request_for_desync',views.request_for_desync,name='request_for_desync'),
    url('^reset_password',views.reset_password,name='reset_password'),
    url('^login',views.login,name='login'),
    url('^logout',views.logout,name='logout'),
    url('^file_upload',views.file_upload,name='file_upload'),
    url('^get_md5',views.get_md5,name='get_md5'),
    url('^file_view',views.file_view,name='file_view'),
    url('^file_download',views.file_download,name='download'),
]

#more ideas :
# deactivate account
