from django.contrib import admin

# Register your models here.
from main_app.models import Profile, StripeKey  #InstagramUser



#admin.site.register(InstagramUser)
admin.site.register(Profile)
admin.site.register(StripeKey)

