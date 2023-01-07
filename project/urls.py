from django.urls import include, path
from rest_framework import routers
from project.views import (
    ContactUsCreateView, 
    LoginView, 
    AreaViewSet, 
    PropertyTypeViewSet,
    ContactInfoAPI,
    AboutUsListingAPIView,
    UserContractViewSet,
    PropertyViewSet
    )

router = routers.DefaultRouter()
router.register("area", AreaViewSet, basename="area")
router.register("property-type", PropertyTypeViewSet, basename="property-type")
router.register("my-unit", UserContractViewSet, basename="user-unit")
router.register("property", PropertyViewSet, basename="property")


urlpatterns = [
    path("", include(router.urls)),
    path("users/login", LoginView.as_view(), name="login"),
    path("contact-us/", ContactUsCreateView.as_view(), name="contact-us"),
    path("contact-us-info/", ContactInfoAPI.as_view(), name="contact-us-info"),
    path("about-us/", AboutUsListingAPIView.as_view(), name="about-us"),
    
]