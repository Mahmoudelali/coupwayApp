from django.db import models
from django.contrib.auth.models import User
from offers.models import Location, Category


class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefered_categories_ids = models.ManyToManyField(Category)


class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isVip = models.BooleanField(default=False)
    locations_ids = models.ManyToManyField(Location)
    preferences_id = models.OneToOneField(Preferences, on_delete=models.CASCADE)
    
    def make_vip(self):
        self.isVip = True
        self.save()
