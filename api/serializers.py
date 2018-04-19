from rest_framework import serializers
from library.models import Books, BookReview, Publication


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = '__all__'


class BookReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReview
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = '__all__'
