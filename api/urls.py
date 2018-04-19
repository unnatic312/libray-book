from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookReviewSerialzerViewSet, BookSerializerViewSet
from rest_framework.authtoken import views

router = DefaultRouter()

router.register('books', BookSerializerViewSet, base_name='books')
router.register('book_review', BookReviewSerialzerViewSet, base_name='book_review')

urlpatterns = [
    path('', include(router.get_urls())),
]
urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token, name='get-auth-token')
]