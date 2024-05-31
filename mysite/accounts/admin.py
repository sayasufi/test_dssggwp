from django.contrib import admin
from .models import Profile, Room, RoomBooking

admin.site.register(Profile)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'description')
    search_fields = ('room_number', 'description')

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_time', 'end_time', 'purpose', 'user')
    search_fields = ('room__room_number', 'purpose', 'user__username')
    list_filter = ('room', 'start_time', 'end_time', 'user')
    date_hierarchy = 'start_time'