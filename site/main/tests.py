from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class SimpleTests(TestCase):

    def test_index_status_code(self):
        # Проверяем, что главная страница возвращает статус 200
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    @patch('main.views.get_info_db')
    def test_report_page_contains_fan_and_water(self, mock_get_info_db):
        mock_get_info_db.return_value = [5083058662, True, False] 
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('fan_on', response.context)
        self.assertIn('water_on', response.context)

    @patch('main.views.connection')
    def test_turn_fan_on_post(self, mock_connection):
        mock_cursor = mock_connection.cursor.return_value.__enter__.return_value
        response = self.client.post(reverse('turn_fan_on'))
        self.assertEqual(response.status_code, 302) 
        mock_cursor.execute.assert_called_with(
            "UPDATE device_states SET fan_on = NOT fan_on WHERE user_id = %s",
            (5083058662,)
        )
