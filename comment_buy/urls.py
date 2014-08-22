from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comment_buy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main_app.views.home', name='home'),
    url(r'token/^$', 'main_app.views.get_access_token', name='get_access_token'),
    url(r'^thank-you/$', 'main_app.views.thank_you', name='thank_you'),
    url(r'^how_it_works/$', 'main_app.views.how_it_works', name='how_it_works'),
    url(r'^for-sale/$', 'main_app.views.all_tagged_for_sale', name='all_tagged_for_sale'),
    url(r'^vendogram-mentions/$', 'main_app.views.vendogram_mentions', name='vendogram_mentions'),
    url(r'^my-media/$', 'main_app.views.my_media', name='my_media'),
    url(r'^following/$', 'main_app.views.following_selling', name='following_selling'),
    url(r'^sold/$', 'main_app.views.sold', name='sold'),
    url(r'^email/$', 'main_app.views.post_email', name='post_email'),
    url(r'^stripe_connect/$', 'main_app.views.stripe_connect', name='stripe_connect'),
    url(r'^armen/$', 'main_app.views.armen', name='armen'),

)
