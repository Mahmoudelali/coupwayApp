from django.db import models
from offers.models import Offer
from django.contrib.auth.models import User
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer")
    redeemed = models.BooleanField(default=False)
    coupons_ordered = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="images/qr_codes/", null=True, blank=True)
    is_gift = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user_id.username

    def redeem(self):
        self.redeemed = True
        self.is_active = False
        self.qr_code = None
        self.save()

    def activate(self):
        self.is_active = True
        try:
            qr_image = qrcode.make(
                f"http://127.0.0.1:8000/api/redeemorder/{self.id}/"
            )

            print(qr_image)
        except Exception as e:
            print(f"Error generating QR code: {e}")

        qr_offset = Image.new("RGB", (400, 400), "white")
        draw_img = ImageDraw.Draw(qr_offset)
        qr_offset.paste(qr_image)
        file_name = f"{self.user_id}.{self.offer_id}.png"
        stream = BytesIO()
        qr_offset.save(stream, "PNG")
        self.qr_code.save(file_name, File(stream), save=False)
        qr_offset.close()
        self.save()

    def save(self, *args, **kwargs):
        # set the user field to the current authenticated user
        if not self.user_id:
            self.user = self.request.user
        super().save(*args, **kwargs)
