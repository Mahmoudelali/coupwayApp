from django.urls import path, include
from . import views

app_name = "api"

urlpatterns = [
    path(
        "registration/",
        include(("registration.urls", "registration"), namespace="registration"),
    ),
    path("getalloffers/", views.getOffers, name="all-offers"),
    path("getalloffers/<int:pk>", views.SingleOfferView.as_view(), name="offer"),
    path(
        "getalloffers/<int:pk>/provide-feedback",
        views.FeedbackView.as_view(),
        name="feedback",
    ),
    path("getvipoffers/", views.getVipOffers, name="vip-offers"),
    path("getnormaloffers/", views.getNormalOffers, name="normal-offers"),
    path("getcategories/", views.getCategories, name="categories"),
    path("getcompanies/", views.getCompanies, name="categories"),
    path("getsubcategories/", views.getSubCategories, name="subcategories"),
    path(
        "getsubcategories/<int:pk>",
        views.getSpecificSubCategories,
        name="subcategories",
    ),
    path("getlocations/", views.getLocations, name="locations"),
    path("createoffer/", views.createOffer, name="create offer"),
    path("createlocation/", views.createLocation, name="create location"),
    path("createcategory/", views.createCategory, name="create category"),
    path("createsubcategory/", views.createSubcategory, name="create subcategories"),
    path("createcompany/", views.createCompany, name="create company"),
    path("giftoffer/", views.createSubcategory, name="gift offer"),
    path("createofferdate/", views.createOfferDate, name="create offerdate"),
    path(
        "makeuservip/<int:userid_to_change>/", views.makeuserVip, name="make user vip"
    ),
    path("createorder/", views.CreateOrderView.as_view(), name="create order"),
    path(
        "redeemorder/<int:order_id>/", views.redeem_order, name="qr code redeem order"
    ),
    path("activateorder/<int:id>/", views.activate_order, name="activate order"),
    path("getuserprofile/", views.getUserProfile, name="get user profile"),
    path("getuserorders/<int:pk>", views.getUserOrders, name="get personal orders"),
    path("getallorders/", views.getAllOrders, name="get all orders"),
    path("getpendingorders/", views.getPendingOrders, name="create order"),
    path("getusergifts/", views.getUserGifts, name="get user gifts"),
    path(
        "ratecompany/<int:company_id>/<int:rate>/",
        views.rate_company,
        name="rate a company",
    ),
    path("searchoffers/", views.searchOffers, name="search offers"),
]
