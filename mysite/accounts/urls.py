from allauth.account.views import LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import RoomViewSet, RoomBookingViewSet, generate_report

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', RoomBookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/generate_report/', generate_report, name='generate_report'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('book_room/', views.book_room, name='book_room'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('accounts/logout/', LogoutView.as_view(template_name='account/logout.html'), name='account_logout'),
]
