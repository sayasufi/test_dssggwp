from rest_framework import serializers

from .models import Room, RoomBooking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = '__all__'

    def validate(self, data):
        room = data.get('room')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if RoomBooking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
        ).exists():
            raise serializers.ValidationError('Комната уже забронирована на это время.')

        return data
