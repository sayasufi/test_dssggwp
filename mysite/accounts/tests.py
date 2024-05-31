from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Room, RoomBooking
from django.urls import reverse
import json

class BookingSystemTestCase(TestCase):
    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

        # Создание комнаты
        self.room = Room.objects.create(room_number=1, description='Описание комнаты 1')

    def test_registration(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешной регистрации

    def test_login(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешного входа

    def test_create_booking(self):
        self.client.login(username='testuser', password='12345')
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        response = self.client.post(reverse('roombooking-list'), {
            'room': self.room.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'purpose': 'Встреча',
            'user': self.user.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Проверка успешного создания бронирования

    def test_double_booking(self):
        self.client.login(username='testuser', password='12345')
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        # Первое бронирование
        self.client.post(reverse('roombooking-list'), {
            'room': self.room.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'purpose': 'Встреча',
            'user': self.user.id
        }, content_type='application/json')
        # Попытка создать второе бронирование на то же время
        response = self.client.post(reverse('roombooking-list'), {
            'room': self.room.id,
            'start_time': (start_time + timezone.timedelta(minutes=30)).isoformat(),
            'end_time': (end_time + timezone.timedelta(minutes=30)).isoformat(),
            'purpose': 'Другая встреча',
            'user': self.user.id
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Проверка на ошибку из-за пересечения бронирований

    def test_get_bookings(self):
        self.client.login(username='testuser', password='12345')
        # Создание бронирования
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        RoomBooking.objects.create(
            room=self.room,
            start_time=start_time,
            end_time=end_time,
            purpose='Встреча',
            user=self.user
        )
        # Запрос списка бронирований
        response = self.client.get(reverse('roombooking-list'))
        self.assertEqual(response.status_code, 200)
        bookings = json.loads(response.content)
        self.assertEqual(len(bookings), 1)  # Проверка количества бронирований

    def test_generate_report(self):
        self.client.login(username='testuser', password='12345')
        # Создание бронирования
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        RoomBooking.objects.create(
            room=self.room,
            start_time=start_time,
            end_time=end_time,
            purpose='Встреча',
            user=self.user
        )
        # Запрос на генерацию отчета
        response = self.client.get(reverse('generate_report'), {
            'start_date': (timezone.now() - timezone.timedelta(days=30)).date().isoformat(),
            'end_date': timezone.now().date().isoformat(),
            'room_id': self.room.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename=booking_report'))

    def test_api_room_creation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('room-list'), {
            'room_number': 2,
            'description': 'Описание комнаты 2'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        room = Room.objects.get(room_number=2)
        self.assertEqual(room.description, 'Описание комнаты 2')

    def test_api_get_rooms(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('room-list'))
        self.assertEqual(response.status_code, 200)
        rooms = json.loads(response.content)
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0]['room_number'], 1)
        self.assertEqual(rooms[0]['description'], 'Описание комнаты 1')

    def test_api_get_bookings_by_date_range(self):
        self.client.login(username='testuser', password='12345')
        start_time = timezone.now() - timezone.timedelta(days=1)
        end_time = timezone.now() + timezone.timedelta(days=1)
        RoomBooking.objects.create(
            room=self.room,
            start_time=start_time,
            end_time=end_time,
            purpose='Встреча',
            user=self.user
        )
        start_date = (timezone.now() - timezone.timedelta(days=2)).date().isoformat()
        end_date = (timezone.now() + timezone.timedelta(days=2)).date().isoformat()
        response = self.client.get(f"/api/bookings/by_date_range/?start_date={start_date}&end_date={end_date}")
        self.assertEqual(response.status_code, 200)
        bookings = json.loads(response.content)
        self.assertEqual(len(bookings), 1)
