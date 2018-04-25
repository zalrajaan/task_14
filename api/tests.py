from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from restaurants.models import Restaurant
from .views import RestaurantListView

class RestaurantAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user = User.objects.create(
            username="bob",
            password='adminadmin',
            is_staff=True,
            )
        self.user.set_password(self.user.password)
        self.user.save()
        self.user2 = User.objects.create(
            username="bob2",
            password='adminadmin',
            )
        self.user2.set_password(self.user2.password)
        self.user2.save()

        self.restaurant_1 = Restaurant.objects.create(
            owner=self.user,
            name="Restaurant 1",
            description="This is Restaurant 1",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )
        self.restaurant_2 = Restaurant.objects.create(
            owner=self.user2,
            name="Restaurant 2", 
            description="This is Restaurant 2",
            opening_time="00:01:00",
            closing_time="23:59:00",
            logo="http://icons.veryicon.com/png/Movie%20%26%20TV/Free%20Star%20Wars/Darth%20Vader.png"
            )

    def test_restaurant_list_view(self):
        list_url = reverse("api-list")
        request = self.factory.get(list_url)
        response = RestaurantListView.as_view()(request)
        self.assertEqual(
            [
                {
                    'name':self.restaurant_1.name,
                    'opening_time': self.restaurant_1.opening_time,
                    'closing_time': self.restaurant_1.closing_time,
                },
                {
                    'name':self.restaurant_2.name,
                    'opening_time': self.restaurant_2.opening_time,
                    'closing_time': self.restaurant_2.closing_time,
                },
            ],
            response.data
        )
        self.assertEqual(response.status_code, 200)