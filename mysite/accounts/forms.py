from django import forms

from .models import Profile, RoomBooking, Room


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['room', 'start_time', 'end_time', 'purpose']
        widgets = {
            'start_time': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
            'end_time': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM'}),
        }
        labels = {
            'room': 'Комната',
            'start_time': 'Время начала',
            'end_time': 'Время окончания',
            'purpose': 'Цель',
        }


class BookingFilterForm(forms.Form):
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=False,
        label='Выберите комнату:',
        empty_label='Все комнаты'
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        label='Дата начала:'
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        label='Дата окончания:'
    )
