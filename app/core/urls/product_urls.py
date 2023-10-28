from django.urls import path
from core.views import product_views as views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products"),
    path("create/", views.ProductCreateView.as_view(), name="create-product"),
    path("upload/", views.uploadImage, name="upload-image"),
    path("top/", views.TopProductView.as_view(), name="top-products"),
    path("<str:pk>/", views.ProductDetailView.as_view(), name="products"),
    path("update/<str:pk>/", views.updateProduct, name="update-product"),
    path("delete/<str:pk>/", views.deleteProduct, name="delete-product"),
    path(
        "category/list/",
        views.CategoryListCreateApiView.as_view(),
        name="category-list-create",
    ),
    path(
        "category/list/<str:pk>/",
        views.CategoryRetrieveUpdateDeleteApiView.as_view(),
        name="category-retrieve-update-delete",
    ),
    path("stock/list/", views.StockListCreateApiView.as_view(), name="stock-list-create"),
    path(
        "stock/list/<str:pk>/",
        views.StockRetrieveUpdateDeleteApiView.as_view(),
        name="stock-retrieve-update-delete",
    ),
]
