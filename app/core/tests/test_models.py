"""Test for models"""
from unittest.mock import patch
from decimal import Decimal
from core import models

from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email="user@example.com", nname="test name", password="testpass123"):
    """create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class TestModels(TestCase):
    """Test models"""

    def test_create_user_with_email_successfull(self):
        """Test creating a user with email is success"""
        email = "test@example.com"
        name = "test name"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            name=name,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email if normalized for new user"""
        sample_emails = [
            ["test1@Example.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises as ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com", "test name", "test123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    @patch("core.models.uuid.uuid4")
    def test_product_file_name_uuid(self, mock_uuid):
        """Test generating image path"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, "exmaple.jpg")
        self.assertEqual(file_path, f"uploads/product/{uuid}.jpg")
