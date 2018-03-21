from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from django.urls import path, include
from django.conf.urls import url

from .serializer_views import product_list, ProductViewset, ProductDetailSerializer, ProductListSerializerGeneric
from .serializer_views import UserDetailSerializer, UserListSerializer, api_root, ServiceViewset, OutputView, SerializedSearchView
from library.views import BookSerializerViewset, BookReviewSerializerViewset, AutherSerializerViewset
from library.views import BookSerializerTemplateView, PublicationSerializerViewset

schema_view = get_schema_view(title='Along With Schema')

router = DefaultRouter()
router.register(r'product', viewset=ProductViewset, base_name='product')
router.register(r'book', viewset=BookSerializerViewset, base_name='book')
router.register(r'book_review', viewset=BookReviewSerializerViewset, base_name='bookreview')
router.register(r'publication', viewset=PublicationSerializerViewset, base_name='publication')
router.register(r'auhter', viewset=AutherSerializerViewset, base_name='auther')
router.register(r'services', viewset=ServiceViewset, base_name='service')
router.register(r'output', viewset=OutputView, base_name='output')


user_serializer_urlpatterns = [
    path('detail/<int:pk>', UserDetailSerializer.as_view(), name='user_serializer_detail'),
    path('list/', UserListSerializer.as_view(), name='user_serializer_list'),
]

product_serializer_urlpatterns = [
    path('detail/<int:pk>', ProductDetailSerializer.as_view(), name='product_serializer_detail'),
    path('list/', ProductListSerializerGeneric.as_view(), name='product_serializer_list_generic'),
]

book_serializer_urlpatterns = [
    path('detail/<int:pk>/', BookSerializerTemplateView.as_view(), name='book_serializer_detail')
]

urlpatterns = [
    path('', api_root, name='serializer_root'),
    path('schema/', schema_view, name='schema'),
    path('list/', product_list, name='product_serializer_list'),
    path('search/', SerializedSearchView.as_view(), name='serialized_search'),
    path('user/', include(user_serializer_urlpatterns)),
    path('product/', include(product_serializer_urlpatterns)),
    path('book/', include(book_serializer_urlpatterns)),
    url('viewset/', include(router.urls)),
]

# For authentication urls login, logout
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

# # For providing format to urls,
# # To use route in urlpatterns, comment out below line
# urlpatterns = format_suffix_patterns(urlpatterns)