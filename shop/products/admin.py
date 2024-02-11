from django.contrib import admin
from .models import Product, Category, Brand, Comments, Filter_Product


class ProductsTabAdmin(admin.TabularInline):
    model = Product
    fields = 'name', 'phone_memory', 'price', 'quantity'
    extra = 1


class CommentTabInline(admin.TabularInline):
    model = Comments
    fields = 'user', 'body', 'active'
    extra = 0




class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount', 'is_have', 'category', 'brand')
    list_editable = ('is_have',)
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [CommentTabInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductsTabAdmin,]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'body', 'created', 'updated', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'body')
    list_editable = ('active',)
    list_display_links = ('user', 'body')


admin.site.register(Comments, CommentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Filter_Product)
