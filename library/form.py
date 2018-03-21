from django.contrib.auth.models import User
from django import forms
from .models import BookReview, Books


class BookReviewForm(forms.ModelForm):

    class Meta:
        model = BookReview
        fields = ('book_review','book',)


class AddBookDetail(forms.ModelForm):

    class Meta:
        model = Books
        fields = ('name','auther','publication','published_on',)


class AddBookData(forms.ModelForm):

    class Meta:
        model = Books
        fields = ('name','auther','publication','published_on','book_data',)


class RegisterForm(forms.ModelForm):

    class Meta():
        model = User
        fields = ('username', 'email','password')