from django.db import models
from offers.models import Offer
from django.contrib.auth.models import User
from r_qrcode.views import generate_qr_code


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer")
    redeemed = models.BooleanField(default=False)
    coupons_ordered = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='/images/qr_codes/', null=True, blank=True)
    is_gift = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def redeem(self):
        self.redeemed = True
        self.is_active = False
        self.qr_code = None
        self.save()

    def activate(self):
        self.is_active = True
        # Generate the QR code
        img = generate_qr_code(self.data)
        # Save the QR code image
        self.qr_code.save(f'{self.data}.png', img, save=False)
        self.save()

    def save(self, *args, **kwargs):
        # set the user field to the current authenticated user
        if not self.user_id:
            self.user = self.request.user
        super().save(*args, **kwargs)
