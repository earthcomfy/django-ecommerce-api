from rest_framework import serializers

from products.models import Product, ProductCategory


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_full_name(self, obj):
        return f'{obj.seller.first_name} {obj.seller.last_name}'


class ProductWriteSerializer(serializers.ModelSerializer):
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = ProductCategoryReadSerializer()

    class Meta:
        model = Product
        fields = ('seller', 'category', 'name', 'desc',
                  'image', 'price', 'quantity',)

    def create(self, validated_data):
        category = validated_data.pop('category')
        instance, created = ProductCategory.objects.get_or_create(**category)
        product = Product.objects.create(**validated_data, category=instance)

        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            nested_serializer = self.fields['category']
            nested_instance = instance.category
            nested_data = validated_data.pop('category')
            nested_serializer.update(nested_instance, nested_data)

        return super(ProductWriteSerializer, self).update(instance, validated_data)
