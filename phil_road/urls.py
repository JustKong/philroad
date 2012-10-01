from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'philroad.views.home'),
    url(r'^fetch/', 'philroad.views.fetch'),
)
