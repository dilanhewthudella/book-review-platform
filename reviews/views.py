from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, ReviewForm
from .models import Book, Review


def home(request):
    featured_books = Book.objects.filter(featured=True)[:3]
    if not featured_books:
        featured_books = Book.objects.all()[:3]

    context = {
        "featured_books": featured_books,
        "book_count": Book.objects.count(),
        "review_count": Review.objects.count(),
    }
    return render(request, "reviews/home.html", context)


def book_list(request):
    query = request.GET.get("q", "").strip()

    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    return render(
        request,
        "reviews/book_list.html",
        {"books": books, "query": query},
    )


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(
        request,
        "reviews/book_detail.html",
        {"book": book},
    )


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save()

            messages.success(
                request,
                f'"{book.title}" was added successfully.'
            )

            return redirect("book_detail", pk=book.pk)

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = BookForm()

    return render(
        request,
        "reviews/book_form.html",
        {
            "form": form,
            "page_title": "Add Book",
            "button_text": "Add Book",
        }
    )


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid():
            book = form.save()

            messages.success(
                request,
                f'"{book.title}" was updated successfully.'
            )

            return redirect("book_detail", pk=book.pk)

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = BookForm(instance=book)

    return render(
        request,
        "reviews/book_form.html",
        {
            "form": form,
            "page_title": "Edit Book",
            "button_text": "Save Changes",
        },
    )


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" was deleted successfully.')
        return redirect("book_list")

    return render(
        request,
        "reviews/confirm_delete.html",
        {
            "object_name": book.title,
            "cancel_url": "book_detail",
            "cancel_pk": book.pk,
        },
    )


def review_list(request):
    reviews = Review.objects.select_related("book", "user")
    return render(
        request,
        "reviews/review_list.html",
        {"reviews": reviews},
    )


def review_create(request, book_id=None):
    initial = {}
    if book_id:
        initial["book"] = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(
                request,
                f'Review for "{review.book.title}" was added successfully.',
            )
            return redirect("book_detail", pk=review.book.pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm(initial=initial)

    return render(
        request,
        "reviews/review_form.html",
        {"form": form, "page_title": "Add Review", "button_text": "Add Review"},
    )


def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, "Review was updated successfully.")
            return redirect("book_detail", pk=review.book.pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "page_title": "Edit Review",
            "button_text": "Save Changes",
        },
    )


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    book_pk = review.book.pk

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review was deleted successfully.")
        return redirect("book_detail", pk=book_pk)

    return render(
        request,
        "reviews/confirm_delete.html",
        {
            "object_name": f"review for {review.book.title}",
            "cancel_url": "book_detail",
            "cancel_pk": book_pk,
        },
    )
