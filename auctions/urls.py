from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("listing/<int:pk>", views.listing_view, name="listing"),
    path("create_listing", views.create_listing_view, name="create_listing")
]
