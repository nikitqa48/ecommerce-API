from django.contrib import admin
from .models import Product,  ProductClass, Attribute
from .models import Stock, Category, ProductCategory, Catalogue, CatalogCategory, ProductAttributeValue, Attribute, Review, ProductImage, ProductRecommendation
from django import forms


class ProductAttributesInline(admin.TabularInline):
    model = Attribute


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


class CategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 0


class ImageForProductInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class CategoryForCatalogInline(admin.TabularInline):
    model = CatalogCategory
    extra = 1


class ProductRecomendationTabular(admin.TabularInline):
    model = ProductRecommendation
    extra = 1
    fk_name = 'primary'
    raw_id_fields = ['primary', 'recommendation']


class CategoryChangeList(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)


class CategoriesForProduct(admin.ModelAdmin):
    model = ProductCategory


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'date_updated', 'rating',  )
    inlines = [ProductAttributeValueInline, CategoryInline, ImageForProductInline, ProductRecomendationTabular]
    exec = 0


@admin.register(Stock)
class AdminStock(admin.ModelAdmin):
    list_display = ('quantity', 'product',)


# @admin.register(AttributeOptionGroup)
# class AttributeOptionGroupAdmin(admin.ModelAdmin):
#     class Meta:
#         model = AttributeOptionGroup
#         fields = ('name',)


@admin.register(Attribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_shipping', 'track_stock')
    # inlines = [ProductAttributesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
   inlines = [CategoryForCatalogInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
# @admin.register(ProductAttributeGroup)
# class AdminAttributeProductGroup(admin.ModelAdmin):
#     pass
#
#
# @admin.register(AttributeGroup)
# class AdminAttributeGroup(admin.ModelAdmin):
#     inlines = [GroupAttributeValueInline]