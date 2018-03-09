from rest_framework import serializers
from .models import Auther, Books, BookReview, Publication


class AutherSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='auther-detail')

    class Meta:
        model = Auther
        fields = (
            'url', 'first_name', 'last_name', 'bio'
        )


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='publication-detail')

    class Meta:
        model = Publication
        fields = ('url', 'name')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    auther = AutherSerializer()
    publication = PublicationSerializer(many=True)

    class Meta:
        model = Books
        fields = (
             'url', 'name', 'auther', 'published_on', 'publication', 'book_data',
        )
        depth = 1

    def create(self, validated_data):
        publications_data = validated_data.pop('publication')
        auther_data = validated_data.pop('auther')
        book = Books.objects.create(**validated_data)
        for publication_data in publications_data:
            Publication.objects.create(book=book, **publication_data)
        Auther.objects.create(book=book, **auther_data)
        return book


class BookReviewSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        many = False,
        slug_field = 'name',
        read_only= True,
    )

    class Meta:
        model = BookReview
        fields = (
            'book_review', 'book', 'date_on',
        )


    def create(self, validate_data):
        book_data = validate_data.pop('book')
        bookreview = BookReview.objects.create(**validate_data)
        Books.objects.create(bookreview=bookreview, **book_data)
        return bookreview




