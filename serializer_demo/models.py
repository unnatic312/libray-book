from django.db import models
from django.utils.translation import gettext as _
from .search import ProductIndex
from elasticsearch_dsl import Index

products = Index('products')
products.settings(
    number_of_shards=1,
    number_of_replicas=0
)

products.aliases(
    old_products={}
)

products.doc_type(ProductIndex)


class ProductSerializerModel(models.Model):
    name = models.CharField(_('Name'), max_length=256)
    price = models.IntegerField(_('Price'))
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='products',)
    description = models.TextField()

    def __str__(self):
        return self.name

    def indexing(self):
        obj = ProductIndex(
            meta={'id':self.id},
            name=self.name,
            price=self.price,
            creator=self.creator.username,
            description=self.description,
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def delete(self,*args, **kwargs):
        current_item = ProductIndex.get(id=self.id)
        current_item.delete()
        super.delete(*args, **kwargs)
        return

    class Meta:
        verbose_name = _('Product')
        ordering = ['name']


class ServiceSerializerModel(models.Model):
    name = models.CharField(_('Name'), max_length=256)
    given_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='services',)
    description = models.TextField(_('Description'))
    days_required = models.IntegerField(_('Days_Required'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        ordering = ['name']