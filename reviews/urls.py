from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "books/",
        views.book_list,
        name="book_list"
    ),

    path(
        "books/add/",
        views.book_create,
        name="book_create"
    ),

    path(
        "books/<int:pk>/",
        views.book_detail,
        name="book_detail"
    ),

    path(
        "books/<int:pk>/edit/",
        views.book_update,
        name="book_update"
    ),

    path(
        "books/<int:pk>/delete/",
        views.book_delete,
        name="book_delete"
    ),

    path(
        "reviews/",
        views.review_list,
        name="review_list"
    ),

    path(
        "reviews/add/",
        views.review_create,
        name="review_create"
    ),

    path(
        "books/<int:book_id>/reviews/add/",
        views.review_create,
        name="review_create_for_book"
    ),

    path(
        "reviews/<int:pk>/edit/",
        views.review_update,
        name="review_update"
    ),

    path(
        "reviews/<int:pk>/delete/",
        views.review_delete,
        name="review_delete"
    ),
]