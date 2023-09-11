from django.db import models
from offers.models import Offer
from django.contrib.auth.models import User
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw
from io import BytesIO


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offer")
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
        """
        # Generate the QR code
 
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
              qr.add_data("https://suckless.org")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        self.qr_code.save(, img, ContentFile(img.tobytes()))

        """
        qr_image = qrcode.make(f"localhost:8000/redeemorder/{self.id}/")
        qr_offset = Image.new("RGB", (410, 410), "white")
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
