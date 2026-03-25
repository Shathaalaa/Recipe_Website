from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class CoreViewTests(TestCase):
    def test_index_page_status_code(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.client.get(reverse("core:index"))
        self.assertTemplateUsed(response, "core/index.html")

    def test_about_page_status_code(self):
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_status_code(self):
        response = self.client.get(reverse("core:contact"))
        self.assertEqual(response.status_code, 200)

    @patch("core.views.send_mail")
    def test_contact_post_valid_data_redirects(self, mock_send_mail):
        mock_send_mail.return_value = 1

        response = self.client.post(
            reverse("core:contact"),
            {
                "name": "john smith",
                "email": "john@example.com",
                "message": "hello there"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(mock_send_mail.call_count, 2)

    @patch("core.views.send_mail")
    def test_contact_post_invalid_data_stays_on_page(self, mock_send_mail):
        response = self.client.post(
            reverse("core:contact"),
            {
                "name": "",
                "email": "not-an-email",
                "message": ""
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_send_mail.call_count, 0)