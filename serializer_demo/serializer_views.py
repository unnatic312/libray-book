# REST framework
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, HttpResponse
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.reverse import reverse


from .models import ProductSerializerModel, ServiceSerializerModel
from .permissions import OwnerOrReadOnlyPermissions
from .serializers import ProductSerializers, UserSerializers, ServiceSerializers

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


@api_view(['GET','POST'])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
@csrf_exempt
def product_list(request):

    if request.method=='GET':
        products = ProductSerializerModel.objects.all()
        serializer = ProductSerializers(products, many=True, context={'request':request})

        return JsonResponse(serializer.data, safe=False)

    elif request.method=='POST':
        serializer = ProductSerializers(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def api_root(request, format=None):
    return Response({
        'user' : reverse('user_serializer_list', request=request, format=format),
        'product' : reverse('product_serializer_list_generic', request=request, format=format),
        'Schema': reverse('schema', request=request, format=format),
        'book': reverse('book-list', request=request, format=format),
    })


class ProductDetailSerializer(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOrReadOnlyPermissions)

    def get(self, request, pk, format=None):
        try:
            product = ProductSerializerModel.objects.get(pk=pk)
        except ProductSerializers.DoesNotExist:
            raise Http404

        serializer = ProductSerializers(product, context={'request':request})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:
            product = ProductSerializerModel.objects.get(pk=pk)
        except ProductSerializerModel.DoesNotExist:
            raise Http404

        serializer = ProductSerializers(product, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            product = ProductSerializerModel.objects.get(pk=pk)
        except ProductSerializerModel.DoesNotExist:
            raise Http404

        serializer = ProductSerializers(product, data=request.data, context={'request':request})
        serializer.delete()

        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class ProductListSerializerGeneric(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOrReadOnlyPermissions)
    queryset = ProductSerializerModel.objects.all()
    serializer_class = ProductSerializers

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProductViewset(viewsets.ModelViewSet):
    queryset = ProductSerializerModel.objects.all()
    serializer_class = ProductSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, OwnerOrReadOnlyPermissions)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UserDetailSerializer(RetrieveAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnlyPermissions)


class UserListSerializer(ListCreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, OwnerOrReadOnlyPermissions)


class ServiceViewset(viewsets.ModelViewSet):
    queryset = ServiceSerializerModel.objects.all()
    serializer_class = ServiceSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(given_by=self.request.user)


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 10
    default_offset = 0


class OutputView(ObjectMultipleModelAPIViewSet):
    pagination_class = LimitPagination
    querylist =[
        {'queryset':ServiceSerializerModel.objects.all(), 'serializer_class':ServiceSerializers},
        {'queryset':ProductSerializerModel.objects.all(), 'serializer_class':ProductSerializers},
    ]


class SerializedSearchView(View):
    client = Elasticsearch()
    s = Search(using=client)

    def post(self, request):
        search_query = request.POST['search']
        data = self.s.query("multi_match", query=search_query, fields=['name', 'description'])
        response = data.execute().hits

        return HttpResponse(response, content_type='application/json')

    def get(self,request):
        template_name = 'serialize_demo/serialized_search.html'
        return render(request, template_name)