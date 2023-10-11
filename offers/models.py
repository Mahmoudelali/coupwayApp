from django.db import models
from django.utils import timezone
from companies.models import Company, Location
from django.contrib.auth.models import User


def offer_image_upload_path(instance, filename):
    print(instance)
    return f"images/offerspics/{instance}/{filename}"


def categories_image_upload_path(instance, filename):
    print(instance)
    return f"images/offerspics/{instance}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    category_illustration = models.ImageField(
        upload_to=categories_image_upload_path, blank=True, null=True
    )

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class DayOfWeek(models.Model):
    DAYS_OF_WEEK_CHOICES = [
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
        ("sunday", "Sunday"),
    ]
    name = models.CharField(
        max_length=20, choices=DAYS_OF_WEEK_CHOICES, default=DAYS_OF_WEEK_CHOICES
    )

    def __str__(self):
        return self.name


class Month(models.Model):
    MONTH_CHOICES = [
        ("january", "January"),
        ("february", "February"),
        ("march", "March"),
        ("april", "April"),
        ("may", "May"),
        ("june", "June"),
        ("july", "July"),
        ("august", "August"),
        ("september", "September"),
        ("october", "October"),
        ("november", "November"),
        ("december", "December"),
    ]
    name = models.CharField(max_length=20, choices=MONTH_CHOICES, default=MONTH_CHOICES)

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=250)
    coupons = models.PositiveIntegerField()
    working = models.BooleanField(default=True)
    main_picture = models.ImageField(upload_to=offer_image_upload_path)
    highlights = models.CharField(max_length=300)
    compensations = models.CharField(max_length=500, default="")
    fine_print = models.CharField(max_length=500, default="")
    description = models.TextField(default="")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    old_price = models.FloatField()
    new_price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategories = models.ManyToManyField(SubCategory)
    isVip = models.BooleanField()
    is_unique = models.BooleanField(default=False)
    days_of_week = models.ManyToManyField(
        "DayOfWeek",
        blank=True,
    )
    months = models.ManyToManyField(
        "Month",
        blank=True,
    )
    start_time = models.TimeField(
        blank=True, null=True  # Allow the field to be empty if not specified
    )
    end_time = models.TimeField(
        blank=True, null=True  # Allow the field to be empty if not specified
    )

    def make_order(self, coupons_to_order):
        self.coupons -= int(coupons_to_order)
        if self.coupons == 0:
            self.working = False
        self.save()

    def __str__(self):
        return self.title


class Feedbacks(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, null=True)
    feedback_content = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username


# offer date is used by the views to determine if an offer is active or not
class OfferDate(models.Model):
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()


# only created in internal offer creation
class Pictures(models.Model):
    parent_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    inner_pic = models.ImageField(upload_to=f"offers/{parent_offer}/")
