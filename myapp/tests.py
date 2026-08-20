from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import EmailAuthenticationBackend, SignUpForm


class AuthenticationTests(TestCase):
	def test_duplicate_email_does_not_crash_authentication(self):
		User.objects.create_user(username='first', email='same@example.com', password='password')
		User.objects.create_user(username='second', email='same@example.com', password='password')

		user = authenticate(
			username='same@example.com',
			password='password',
			backend=EmailAuthenticationBackend(),
		)

		self.assertIsNone(user)

	def test_signup_rejects_existing_email(self):
		User.objects.create_user(username='existing', email='same@example.com', password='password')

		form = SignUpForm(data={
			'full_name': 'New User',
			'email': 'SAME@example.com',
			'password': 'password',
			'password_confirm': 'password',
		})

		self.assertFalse(form.is_valid())
		self.assertIn('already exists', form.errors['email'][0])
