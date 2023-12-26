# from django.contrib.auth.models import User
from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


# class ShopAllSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         return models.Shop.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.desc = validated_data.get('desc', instance.desc)
#         instance.save()
#         return instance

#     class Meta:
#         model = models.Shop
#         fields = '__all__'


class ProductAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ShopAllSerializer(serializers.ModelSerializer):
    # products = ProductAllSerializer(many=True, read_only=True)
    bajins = serializers.SerializerMethodField()

    class Meta:
        model = models.Shop
        fields = ['id', 'name', 'bajins']

    @staticmethod
    def get_bajins(obj):
        products = models.ShopBajin.objects.filter(shop=obj)
        return ProductAllSerializer(products, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['product', 'price', 'id']


class BajinSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = models.ShopBajin
        fields = ['id', 'name', 'products']

    @staticmethod
    def get_products(obj):
        products = models.Product.objects.filter(bajin=obj)
        return ProductSerializer(products, many=True).data


class ShopSerializer(serializers.ModelSerializer):
    bajins = serializers.SerializerMethodField()

    class Meta:
        model = models.Shop
        fields = ['name', 'bajins']

    @staticmethod
    def get_bajins(obj):
        bajins = models.ShopBajin.objects.get(id=2)
        return BajinSerializer(bajins).data


class ProductNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class BajinNewSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = models.ShopBajin
        fields = ["id", "name", "shop", "products"]

    @staticmethod
    def get_products(obj):
        products = models.Product.objects.get("price")
        return ProductNewSerializer(products, many=True).data


class ProductImageSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImages
        fields = ['id', 'image']


class ProductNew2Serializator(serializers.ModelSerializer):
    images = ProductImageSerializator(many=True, required=False)

    class Meta:
        model = models.Product
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImages
        fields = ['id', 'product', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class BajinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopBajin
        fields = '__all__'


class ProductSer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()


# class UserTokenSerializer(serializers.ModelSerializer):
#     tokens = TokenSerializer()
#     class Meta:
#         model = models.UserToken
#         fields = ["user", "tokens"]


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "access_token", "refresh_token"]
        extra_kwargs = {
            'access_token': {'write_only': False},  # Токены не будут отображаться при сериализации
            'refresh_token': {'write_only': False}
        }

    def update(self, instance, validated_data):
        # Обновление полей access_token и refresh_token при сохранении пользователя
        instance.access_token = validated_data.get('access_token', instance.access_token)
        instance.refresh_token = validated_data.get('refresh_token', instance.refresh_token)
        instance.save()
        return instance

# class ShopOnlyIdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Shop
#         fields = ['id']







