from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Snack


# Create your tests here.


class SnackTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@@test.com',
            password='test@12345'
        )
        self.Snack = Snack.objects.create(
            name="Test",
            rank=10,
            reviewer=self.user,
        )

    def test_list_status(self):
        url = reverse("Snacks_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_template(self):
        url = reverse("Snacks_list")
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'Snacks_list.html')

    def test_str_method(self):
        self.assertEqual(str(self.Snack), 'Test')

    def test_detail_view(self):
        url = reverse('Snack_detail', args=[self.Snack.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Snack_detail.html')

    def test_create_view(self):
        url = reverse('Snack_create')
        data = {
            "name": "Test Create",
            "reviewer": self.user.id
        }
        response = self.client.post(path=url, data=data, follow=True)
        self.assertTemplateUsed(response, 'Snack_detail.html')
        self.assertRedirects(response, reverse('Snack_detail', args=[2]))
        self.assertEqual(len(Snack.objects.all()), 2)
