from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', FitnessClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('userregistration/', RegisterUserView.as_view(), name='registration'),
    path('userlogin/', LoginUserView.as_view(), name='login'),
    path('availableclasses/', AvailableClasses.as_view(), name='classes'),
    path('slotbooking/', BookSlotView.as_view(), name='booking'),
    path('bookings/<str:user_email>/', GetSpecificBooking.as_view(), name='viewbookings'),  
]
