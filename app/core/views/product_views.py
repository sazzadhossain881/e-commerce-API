from django.shortcuts import render

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action, APIView

from core import permissions
from core import models
from core import serializers
from core.authentication import (
    JWTAuthentication,
)


class TopProductView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get_queryset(self):
        return models.Product.objects.filter(rating__gt=4).order_by("-rating")[0:5]


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get_queryset(self):
        return models.Product.objects.all()


class ProductListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    def get_queryset(self):
        return models.Product.objects.all().order_by("-id")


class ProductCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        permissions.IsAdminOrReadOnly,
    ]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """retrieve product for the user"""
        return models.Product.objects.all().order_by("-id")

    def perform_create(self, serializer):
        """create a new product"""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """upload an image to product"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def updateProduct(request, pk):
    data = request.data

    product = models.Product.objects.get(id=pk)

    product.name = data["name"]
    product.price = data["price"]
    product.brand = data["brand"]
    product.countInStock = data["countInStock"]
    product.category = data["category"]
    product.description = data["description"]

    product.save()
    serializer = serializers.ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def deleteProduct(request, pk):
    product = models.Product.objects.get(id=pk)
    product.delete()
    return Response("Product deleted")


@api_view(["POST"])
def uploadImage(request):
    data = request.data

    product_id = data["product_id"]

    product = models.Product.objects.get(id=product_id)
    product.image = request.FILES.get("image")
    product.save()
    return Response("image was uploaded")


class CategoryListCreateApiView(APIView):
    """category list create api view"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        category = models.Category.objects.all()
        serializer = serializers.CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class CategoryRetrieveUpdateDeleteApiView(APIView):
    """category retrieve update delete api view"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            category = models.Category.objects.get(pk=pk)
        except models.Category.DoesNotExist():
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CategorySerializer(category, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        category = models.Category.objects.get(pk=pk)
        serializer = serializers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categoty = models.Category.objects.get(pk=pk)
        categoty.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StockListCreateApiView(APIView):
    """category list create api view"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        stock = models.Stock.objects.all()
        serializer = serializers.StockSerializer(stock, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StockRetrieveUpdateDeleteApiView(APIView):
    """category retrieve update delete api view"""

    def get(self, request, pk):
        try:
            stock = models.Stock.objects.get(pk=pk)
        except models.Stock.DoesNotExist():
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.StockSerializer(stock, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        stock = models.Stock.objects.get(pk=pk)
        serializer = serializers.StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stock = models.Stock.objects.get(pk=pk)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
