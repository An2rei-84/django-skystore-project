from django.contrib import admin
from .models import Product, Category, Contact, Feedback


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Category.
    """
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Product.
    """
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Contact.
    """
    list_display = ('country', 'inn', 'address',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Feedback.
    """
    list_display = ('name', 'phone', 'created_at',)
