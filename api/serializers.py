from rest_framework import serializers
from offers.models import Offer, OfferDate, Category, Pictures, Feedbacks, SubCategory
from companies.models import Location, Company
from datetime import datetime

from registration.models import AdditionalUserInfo
from django.contrib.auth.models import User


class OfferDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDate
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalUserInfo
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
            "location_description",
            "city",
            "review",
            "reviews_count",
        ]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["name", "id"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories", "category_illustration"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["name", "lng", "lat"]


class OffersSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.main_picture.url)
        return obj.image.url  # Fallback if request is not available

    class Meta:
        model = Offer
        fields = "__all__"
        depth = 2
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    offer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Feedbacks
        fields = ["id", "user_id", "feedback_content", "offer_id", "user"]


class SingleOfferCategory(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SingleOfferSerializer(serializers.ModelSerializer):
    subcategory_names = serializers.SerializerMethodField(method_name='get_subcategory_names')
    location = LocationSerializer()
    company = CompanySerializer()
    category = SingleOfferCategory()
    feedback = FeedbackSerializer(many=True, allow_null=True)

    class Meta:
        model = Offer
        fields = "__all__"

    def get_subcategory_names(self, obj):
        return [subcategory.name for subcategory in obj.subcategories.all()]


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = "__all__"
