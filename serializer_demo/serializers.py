from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProductSerializerModel, ServiceSerializerModel


class ProductSerializers(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    url = serializers.HyperlinkedIdentityField(view_name='product_serializer_detail')
    class Meta:
        model = ProductSerializerModel
        fields = (
            'id', 'name', 'price', 'creator', 'description', 'url',
        )


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'products',
        )
        depth = 1


class ServiceSerializers(serializers.HyperlinkedModelSerializer):
    given_by = serializers.ReadOnlyField(source='given_by.username')
    url = serializers.HyperlinkedIdentityField(view_name='service-detail')

    class Meta:
        model = ServiceSerializerModel
        fields = (
             'url', 'id', 'name', 'given_by', 'days_required', 'description',
        )