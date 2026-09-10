from datetime import date

from django import forms

from .models import Book, Review


class BookForm(forms.ModelForm):

    class Meta:
        model = Book

        fields = [
            "title",
            "author",
            "genre",
            "publication_date",
            "description",
            "featured",
            "image",
        ]

        widgets = {
            "publication_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"

            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"

            else:
                field.widget.attrs["class"] = "form-control"

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 2:
            raise forms.ValidationError(
                "Book title must contain at least 2 characters."
            )

        return title

    def clean_author(self):
        author = self.cleaned_data["author"].strip()

        if len(author) < 2:
            raise forms.ValidationError(
                "Author name must contain at least 2 characters."
            )

        return author

    def clean_publication_date(self):
        publication_date = self.cleaned_data["publication_date"]

        if publication_date > date.today():
            raise forms.ValidationError(
                "Publication date cannot be in the future."
            )

        return publication_date


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "user",
            "book",
            "rating",
            "comment",
        ]

        widgets = {

            "comment": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Write your review here...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"

            else:
                field.widget.attrs["class"] = "form-control"

    def clean_comment(self):
        comment = self.cleaned_data["comment"].strip()

        if len(comment) < 10:
            raise forms.ValidationError(
                "Review must contain at least 10 characters."
            )

        return comment