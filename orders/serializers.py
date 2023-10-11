from rest_framework import serializers
from api.serializers import OffersSerializer, SingleOfferSerializer
from .models import Order


class OrdersSerializer(serializers.ModelSerializer):
    offer = OffersSerializer(read_only=True)
    offer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "redeemed",
            "coupons_ordered",
            "order_date",
            "qr_code",
            "is_gift",
            "is_active",
            "user_id",
            "offer_id",
            "offer",
        ]


class OrdersListSerializer(serializers.ListSerializer):
    child = OrdersSerializer()
