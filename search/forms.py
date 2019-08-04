from django import forms
from .models import Book

class BookForm(forms.Form):
    book_title = forms.CharField(label='책 제목', max_length=200)