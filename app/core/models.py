import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


def product_image_file_path(instance, filename):
    """Generate file path for new banner image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "product", filename)


# Create your models here..
class UserProfileManager(BaseUserManager):
    """manager for user profile"""

    def create_user(self, email, name, password=None):
        """create save and return a new user"""
        if not email:
            raise ValueError("user must have an email address")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create and return a new superuser"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """user in the system"""

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = "email"

    def get_short_name(self):
        """retrieve short name of the user"""
        return self.name

    def get_full_name(self):
        """retrieve full name of the user"""
        return self.name

    def __str__(self):
        """string representation of the user"""
        return self.email


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()


class Category(models.Model):
    """category objects"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    """stock objects"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    countInStock = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.countInStock)


class Product(models.Model):
    """creating product model"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )

    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, upload_to="product_image_file_path")
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name="product_category"
    )
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    newReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    stock = models.OneToOneField(
        "Stock", on_delete=models.SET_NULL, null=True, related_name="product_stock"
    )
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
