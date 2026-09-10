from django.contrib import admin
from .models import Book, Review, User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email"
    )

    search_fields = (
        "name",
        "email"
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "genre",
        "publication_date",
        "featured"
    )

    list_filter = (
        "genre",
        "featured"
    )

    search_fields = (
        "title",
        "author"
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "book",
        "user",
        "rating",
        "created_at"
    )

    list_filter = (
        "rating",
    )

    search_fields = (
        "book__title",
        "user__name",
        "comment"
    )