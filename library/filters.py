import django_filters
from .models import Books, BookReview, Auther, Publication


class BookFilter(django_filters.FilterSet):

    class Meta:
        model = Books
        fields = {
            'name':['contains',],
        }