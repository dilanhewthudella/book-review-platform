from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)

    image = models.ImageField(
        upload_to="book_covers/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def average_rating(self):
        ratings = self.reviews.values_list(
            "rating",
            flat=True
        )

        if not ratings:
            return None

        return round(sum(ratings) / len(ratings), 1)

class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews",
    )


    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.book.title} - {self.rating}/5 by {self.user.name}"