from rest_framework import serializers

from ..models import Category, Smartphone


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug',
        ]


class BaseProductSerializer:

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField()
    slug = serializers.SlugField()
    image = serializers.ImageField()
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)


class SmartphoneSerializer(BaseProductSerializer, serializers.ModelSerializer):

    diagonal = serializers.CharField()
    display_type = serializers.CharField()
    resolution = serializers.CharField()
    accum_value = serializers.CharField()
    ram = serializers.CharField()
    sd = serializers.BooleanField()
    sd_volume_max = serializers.CharField(required=False)
    main_cam_mp = serializers.CharField()
    frontal_cam_mp = serializers.CharField()

    class Meta:
        model = Smartphone
        fields = '__all__'
