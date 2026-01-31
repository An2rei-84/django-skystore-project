from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    ProductListView, ContactFormView, ProductDetailView,
    ProductCreateView, ProductUpdateView, ProductDeleteView, unpublish_product,
    CategoryProductListView
)

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactFormView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('category/<int:pk>/', CategoryProductListView.as_view(), name='category_products'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/unpublish/', unpublish_product, name='unpublish_product'),
]
