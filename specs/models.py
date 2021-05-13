from django.db import models


class CategoryFeature(models.Model):

    category = models.ForeignKey('store.Category', verbose_name='Category', on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100, verbose_name='Feature name')
    feature_filter_name = models.CharField(max_length=50, verbose_name='Filter name')
    unit = models.CharField(max_length=50, verbose_name='Measure unit', null=True, blank=True)

    class Meta:
        unique_together = {'category', 'feature_name', 'feature_filter_name'}

    def __str__(self):
        return f'{self.category.name} | {self.feature_name}'


class FeatureValidator(models.Model):

    category = models.ForeignKey('store.Category', verbose_name='Category', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Feature key', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100, verbose_name='Valid value')

    def __str__(self):
        return f'Category "{self.category.name}"' \
               f'Feature "{self.feature_key.feature_name}"' \
               f'Valid value "{self.valid_feature_value}"'


class ProductFeatures(models.Model):

    product = models.ForeignKey('store.Product', verbose_name='Product', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Feature', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Value')

    def __str__(self):
        return f'Product - "{self.product.title}"' \
               f'Feature - "{self.feature.name}"' \ 
               f'Value - "{self.value}"'