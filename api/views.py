from offers.models import (
    Offer,
    OfferDate,
    Category,
    # Subcategory,
    Location,
    Pictures,
    Feedbacks,
)
from orders.models import Order
from registration.models import Preferences
from companies.models import Company
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from registration.models import AdditionalUserInfo
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .serializers import (
    OffersSerializer,
    CompanySerializer,
    CategorySerializer,
    LocationSerializer,
    OfferDateSerializer,
    UserInfoSerializer,
    SingleOfferSerializer,
    FeedbackSerializer,
)
from orders.serializers import OrdersListSerializer, OrdersSerializer


@api_view(["GET"])
def getOffers(request):
    products = Offer.objects.filter(working=True)
    serializer = OffersSerializer(products, many=True, context= { "request" : request})
    return Response(serializer.data)


class SingleOfferView(generics.RetrieveAPIView):
    def get_queryset(self):
        pk = self.kwargs["pk"]
        queryset = Offer.objects.filter(id=pk)
        return queryset

    serializer_class = SingleOfferSerializer


class FeedbackView(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedbacks.objects.all()

    def get(self, request, pk):
        # select the related offer
        offer = get_object_or_404(Offer, pk=pk)
        # Get all feedbacks related to the offer
        feeds = Feedbacks.objects.filter(offer_id=offer)
        serialized_item = FeedbackSerializer(feeds, many=True)
        return Response(serialized_item.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        print(request.data)
        serialized_item = FeedbackSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()

        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view(["GET"])
def getNormalOffers(request):
    products = Offer.objects.filter(isVip=False)
    serializer = OffersSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getVipOffers(request):
    products = Offer.objects.filter(isVip=True)
    serializer = OffersSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getCompanies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getSubCategories(request):
    subcategories = Subcategory.objects.all()
    serializer = SubcategorySerializer(subcategories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getSpecificSubCategories(request, pk):
    subcategories = Subcategory.objects.all().filter(id=pk)
    if len(subcategories) == 0:
        return Response({"message": "not found"}, status.HTTP_404_NOT_FOUND)
    serializer = SubcategorySerializer(subcategories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getLocations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)


# the admin api
# -----------------


@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def createOffer(request):
    serializer = OffersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create location / category / sub / company


@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def createLocation(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def createCategory(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def createSubcategory(request):
    serializer = SubcategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def createCompany(request):
    # some of the company fields are automatically added
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# gift offers for users
@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def giftOffer(request):
    serializer = OrdersSerializer(data=request.data)
    if serializer.is_valid():
        offer_id = request.data.offer_id
        offer = Offer.objects.get(pk=offer_id)
        if offer.is_unique and request.data.coupons_ordered > 1:
            return Response(
                {"message": "u can't take multiple coupons of this order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        offer_dates = OfferDate.objects.filter(offer_id=offer_id)
        for offerdate in offer_dates:
            offer_active = offerdate.startdate <= timezone.now() <= offerdate.enddate
            if not offer_active:
                offer.working = False
                offer.save()
            offer.working = True
        offer.make_order(coupons_to_order=request.data.coupons_ordered)
        serializer.save()
        order = Order.objects.get(pk=serializer.data.id)
        order.activate()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create the offer date (should be created after offer creation)
@user_passes_test(lambda u: u.is_superuser)
@api_view(["POST"])
def createOfferDate(request):
    serializer = OfferDateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# mark user as vip
@api_view(["GET"])
def makeuserVip(request, userid_to_change):
    if request.user.is_superuser:
        user = AdditionalUserInfo.objects.get(user=userid_to_change)
        user.make_vip()
        user.save()
        return Response({"message": "user made vip successfuly"})
    return Response({"message": "error : u must be admin to change users status"})


# users api
# ----------


@login_required(login_url="/api/registration/accounts/login/")
@api_view(["POST"])
def createOrder(request):
    serializer = OrdersSerializer(data=request.data)
    if serializer.is_valid():
        offer_id = request.data["offer_id"]
        offer = Offer.objects.get(id=offer_id)
        if offer.is_unique and request.data["coupons_ordered"] > 1:
            return Response(
                {"message": "u can't take multiple coupons of this order"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        offer_dates = OfferDate.objects.filter(offer_id=offer_id)
        for offerdate in offer_dates:
            offer_active = offerdate.startdate <= timezone.now() <= offerdate.enddate
            if not offer_active:
                offer.working = False
                offer.save()
            offer.working = True
        offer.make_order(coupons_to_order=request.data["coupons_ordered"])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class CreateOrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer(many=True)

    def post(self, request, format=None):
        data = request.data
        serializer = OrdersSerializer(data=data, many=True)
        for i in range(len(data)):
            if serializer.is_valid():
                offer_id = request.data[i]["offer_id"]
                offer = Offer.objects.get(id=offer_id)
                if offer.is_unique and int(request.data[i]["coupons_ordered"]) > 1:
                    return Response(
                        {"message": "You can't take multiple coupons of this order"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                offer_dates = OfferDate.objects.filter(offer_id=offer_id)
                for offerdate in offer_dates:
                    offer_active = (
                        offerdate.startdate <= timezone.now() <= offerdate.enddate
                    )
                    if not offer_active:
                        offer.working = False
                        offer.save()
                    offer.working = True
                offer.make_order(coupons_to_order=request.data[i]["coupons_ordered"])
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# redeem order


@api_view(["GET"])
@permission_classes([IsAdminUser])
def redeem_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if not order.redeemed:
        order.redeem()
    return Response({"message": "Order redeemed"})


# activate_order


@api_view(["GET"])
def activate_order(request, id):
    if request.user.is_superuser:
        order = Order.objects.get(id=id)
        order.activate()
        return Response({"message": "Order activated successfuly"})
    return Response({"message": "only admin can activate offers"})


# get user info
@login_required(login_url="/api/registration/accounts/login/")
@api_view(["GET"])
def getUserProfile(request):
    profile = AdditionalUserInfo.objects.get(user=request.user.id)
    serializer = UserInfoSerializer(profile)
    return Response(serializer.data)


# get orders


# @login_required(login_url="/api/registration/accounts/login/")
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getAllOrders(request):
    orders = Order.objects.all()
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getPendingOrders(request):
    orders = Order.objects.filter(is_active=False)
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


# @login_required(login_url="/api/registration/accounts/login/")
@api_view(["GET"])
def getUserOrders(request, pk):
    print(request.user.id)
    orders = Order.objects.filter(user_id=pk)
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


# get gifts


@login_required(login_url="/api/registration/accounts/login/")
@api_view(["GET"])
def getUserGifts(request):
    orders = Order.objects.filter(user_id=request.user.id, is_gift=True)
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


# users review / rating api for companies
@api_view(["GET"])
def rate_company(request, company_id, rate):
    user = request.user
    if not user.is_authenticated:
        return Response(
            {"error": "You must be logged in to rate a company."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return Response(
            {"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND
        )

    rating_value = rate
    if rating_value < 1 or rating_value > 5:
        return Response(
            {"error": "Rating value must be between 1 and 5."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    company.reviews_count += 1
    company.review = int((company.review + rating_value) / company.reviews_count)
    company.save()

    return Response(
        {"message": "Rating saved successfully."}, status=status.HTTP_200_OK
    )


# search


# @api_view(["GET"])
# def searchOffers(request, query):
#     offers = Offer.objects.filter(Q(title__icontains=query) & Q(working=True))
#     serializer = OffersSerializer(offers, many=True)
#     return Response(serializer.data)


@api_view(["GET"])
def searchOffers(request):
    id = request.GET.get("id")
    queryset = request.GET.get("queryset")
    location = request.GET.get("location")

    if request.GET is not None:
        if location and queryset:
            offers = (
                Offer.objects.all()
                .filter(Q(working=True))
                .filter(Q(location__name__icontains=location))
            ).filter(
                Q(title=queryset)
                | Q(category__name__icontains=queryset)
                | Q(subcategories__name__icontains=queryset)
            )
            serializer = SingleOfferSerializer(offers, many=True)
            return Response(serializer.data)
        if location:
            offers = (
                Offer.objects.all()
                .filter(Q(working=True))
                .filter(Q(location__name__icontains=location))
            )
            serializer = SingleOfferSerializer(offers, many=True)
            return Response(serializer.data)
        else:
            offers = (
                Offer.objects.all()
                .filter(Q(working=True))
                .filter(
                    Q(title__icontains=queryset)
                    | Q(category__name__icontains=queryset)
                    | Q(subcategories__name__icontains=queryset)
                )
            )
            serializer = SingleOfferSerializer(offers, many=True)
            return Response(serializer.data)
    else:
        return Response({"message": "No query parameter found."})




# LoginView

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def LoginView(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")