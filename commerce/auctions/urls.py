from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/add", views.add_watchlist, name="add_watchlist"),
    path("watchlist/<int:listing_id>/remove", views.remove_watchlist, name="remove_watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    # path("bid/<int:listing_id>", views.bid, name="bid"),
    # path("close/<int:listing_id>", views.close, name="close"),

]
