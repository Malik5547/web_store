from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass

class MaxImageSizeErrorException(Exception):
    pass


class LatestProductsManager:

    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                return sorted(
                    products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                )

        return products


class LatestProducts:

    objects = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (900, 900)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if image.size > self.MAX_IMAGE_SIZE:
            raise MaxImageSizeErrorException('Image size should not be bigger than 3MB.')
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Image resolution is smaller than minimal.')
        if img.height > max_height or img.widtg > max_width:
            raise MaxResolutionErrorException('Image resolution is bigger than maximal.')
        return image



class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Display type')
    cpu_freq = models.CharField(max_length=255, verbose_name='CPU Frequency')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    video = models.CharField(max_length=255, verbose_name='Video card')
    time_without_charge = models.CharField(max_length=255, verbose_name='Time without charging')

    def __str__(self):
        return '{} : {}'.format(self.category, self.title)


class Smartphone(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Display type')
    resolution = models.CharField(max_length=255, verbose_name='Display resolution')
    accum_value = models.CharField(max_length=255, verbose_name='Accumulator value')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='SD maximal volume')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Main camera')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Frontal camera')

    def __str__(self):
        return '{} : {}'.format(self.category, self.title)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return 'Cart product: {}'.format(self.product.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Owner', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return str(self.id)


class Specification(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, verbose_name='Name of specification product')

    def __str__(self):
        return 'Specification for product: {}'.format(self.name)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone')
    address = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return 'Customer: {} {}'.format(self.user.first_name, self.user.last_name)
