from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class UserAccountTests(TestCase):
    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            username='Vale', email='vale@cq.com', first_name='Valentina', last_name='Fernandez', password='password'
        )
        self.assertEqual(user.email, 'vale@cq.com')
        self.assertEqual(user.username, 'Vale')
        self.assertEqual(user.first_name, 'Valentina')
        self.assertEqual(user.last_name, 'Fernandez')
        self.assertEqual(str(user), 'Vale')

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', username='devrrior', first_name='first_name', last_name='hoal', password='password')
