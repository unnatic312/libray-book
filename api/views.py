from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import BookSerializer, BookReviewSerializer
from library.models import Books, BookReview


class BookSerializerViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Books.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class BookReviewSerialzerViewSet(ModelViewSet):
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)