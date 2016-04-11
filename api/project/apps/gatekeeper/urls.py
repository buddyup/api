from django.conf.urls import patterns, include, url
from django.contrib import admin
from gatekeeper import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^auth$', views.user_authenticate, name='authenticate'),
    url(r'^auth/signup$', views.user_signup, name='signup'),
    url(r'^auth/change-password$', views.change_password, name='change_password'),
    url(r'^auth/check-new-account$', views.check_new_account, name='check_new_account'),
    url(r'^reset-password$', views.reset_password, name='reset_password'),
    url(r'^auth/confirm-delete$', views.confirm_delete, name='confirm_delete'),
    url(r'^auth/confirm/(?P<email_key>[\w-]+)/?$', views.confirm_email, name='confirm_email'),
    url(r'^confirm-reset/(?P<email_key>[\w-]+)/$', views.confirm_reset, name='confirm_reset'),
    url(r'^internal/migrate-user$', views.migrate_user, name='migrate_user'),
    url(r'^internal/migrate-picture$', views.migrate_picture, name='migrate_picture'),
    url(r'^internal/merge-classes$', views.handle_merge_class_request, name='merge_classes'),
)
