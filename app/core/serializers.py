from rest_framework import serializers
from core import models


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user"""

    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.User
        fields = ["id", "name", "email", "password", "isAdmin"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def get_isAdmin(self, obj):
        return obj.is_staff

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    """serialize products"""

    class Meta:
        model = models.Product
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class ProductImageSerializer(serializers.ModelSerializer):
    """serializer for uploading image to product"""

    class Meta:
        model = models.Product
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "image": {
                "required": True,
            }
        }


class CategorySerializer(serializers.ModelSerializer):
    """serializer for the category objects"""

    class Meta:
        model = models.Category
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class StockSerializer(serializers.ModelSerializer):
    """serializer for stock objects"""

    class Meta:
        model = models.Stock
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(StockSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1
