from django.contrib.auth.models import User
from django import forms
from .models import BookReview, Books, Auther


class BookReviewForm(forms.ModelForm):

    class Meta:
        model = BookReview
        fields = ('book_review','book',)


class AddBookData(forms.ModelForm):

    class Meta:
        model = Books
        fields = ('name','auther','publication','published_on','book_data',)


class RegisterForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username', 'email','password')


class AddAutherForm(forms.ModelForm):
    class Meta():
        model = Auther
        fields = ('first_name', 'last_name', 'bio')