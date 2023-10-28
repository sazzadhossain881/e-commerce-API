from django.urls import path
from core.views import user_views as views

urlpatterns = [
    path("login/", views.LoginApiView.as_view(), name="login"),
    path("register/", views.RegisterApiView.as_view(), name="register"),
    path("profile/", views.UserApiView.as_view(), name="user-profile"),
    path("", views.UsersApiView.as_view(), name="users"),
    path("<str:pk>/", views.RetrieveUserApiView.as_view(), name="user"),
    path("update/<str:pk>/", views.UpdateApiView.as_view(), name="user-update"),
    path("delete/<str:pk>/", views.DeleteApiView.as_view(), name="user-delete"),
    path("refresh/", views.RefreshApiView.as_view(), name="refresh"),
    path("logout/", views.LogoutApiView.as_view(), name="logout"),
]
