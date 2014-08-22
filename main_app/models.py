from django.contrib.auth.models import User
from django.db import models


# Should extend AbstractUser or have a ForeignKey to user
# If you got python-social-auth working, this would have been easier to manage too
class Profile(models.Model):
    # user = models.OneToOneField(User)
    bio = models.CharField(max_length=2200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    instagram_id = models.CharField(max_length=10, unique=True)
    access_token = models.TextField()
    email = models.EmailField(default="armenlsuny@gmail.com")
    user = models.CharField(max_length=30)
   # instagram_username = models.CharField(max_length=30)
    def __unicode__(self):
        return u'{}'.format(self.instagram_id)


class StripeKey(models.Model):
    user = models.ForeignKey(Profile, related_name="stripe_key_profile")
    stripe_key = models.CharField(max_length=100)

# the bellow is my old non working shit.

# class UserManager(BaseUserManager):
#     def _create_user(self, instagram_id, password,):
#         # if not username:
#         #     raise ValueError(_("given nme is already takne"))
#         # email = self.normalize_email(email)
#         user = self.model(instagram_id, password)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, instagram_id, password=None):
#         return self._create_user(instagram_id, password)
#     def create_superuser(self, instagram_id, password):
#         user=self._create_user(instagram_id, password,)
#         user.is_active=True
#         user.is_staff=True
#         user.save(using=self._db)
#         return user
#
# class InstagramUser(AbstractBaseUser):
#     bio = models.CharField(max_length=2200, blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#     profile_picture = models.URLField(blank=True, null=True)
#     full_name = models.CharField(max_length=100, blank=True, null=True)
#     instagram_id = models.CharField(max_length=10, unique=True)
#     access_token = models.TextField()
#
#     is_staff = models.BooleanField(('staff status'), default=False,)
#     # help_text=_('Designates whether the user can log into this admin site.'))
#     is_active = models.BooleanField(('active'), default=False,)
#     # help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
#
#     instagram_username = models.CharField(max_length=30, default='bob')
#     USERNAME_FIELD = 'instagram_id'
#
#     objects = UserManager()
