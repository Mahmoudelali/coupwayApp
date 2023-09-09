from django.db import models
from django.utils import timezone
from companies.models import Company, Location
from django.contrib.auth.models import User


# class Subcategory(models.Model):
#     name = models.CharField(max_length=50)

#     class Meta:
#         # this goes for plural queryset name in db retrieving
#         verbose_name_plural = "subcategories"

#     def __str__(self) -> str:
#         return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=50)
#     Subcategories = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)

#     class Meta:
#         verbose_name_plural = "categories"

#     def __str__(self) -> str:
#         return self.name


# v2
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


def offer_image_upload_path(instance, filename):
    return f"images/offerspics/{instance.id}/{filename}"


class Offer(models.Model):
    title = models.CharField(max_length=250)
    coupons = models.PositiveIntegerField()

    # mark this as false to make the offer unsendable to the mainpage
    working = models.BooleanField(default=True)
    main_picture = models.ImageField(upload_to=offer_image_upload_path)

    # small and detailed description for the offer
    highlights = models.CharField(max_length=300)
    compensations = models.CharField(max_length=500, default="")
    fine_print = models.CharField(max_length=500, default="")
    description = models.TextField(default="")

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    # maybe return the difference of price
    old_price = models.FloatField()
    new_price = models.FloatField()

    # make this a list maybe we need category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    isVip = models.BooleanField()

    # a single user cannot take multiple coupons of a unique offer
    is_unique = models.BooleanField(default=False)

    # Subcategory connected to the offer
    # sub = models.ManyToManyField(Subcategory)

    def make_order(self, coupons_to_order):
        self.coupons -= int(coupons_to_order)
        self.save()

    def __str__(self):
        return self.title


class Feedbacks(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, null=True)
    feedback_content = models.CharField(max_length=500, null=True, blank=True)


# offer date is used by the views to determine if an offer is active or not
class OfferDate(models.Model):
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()


# only created in internal offer creation
class Pictures(models.Model):
    parent_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    inner_pic = models.ImageField(upload_to=f"offers/{parent_offer}/")
