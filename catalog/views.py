from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Product, Contact
from .forms import ProductForm

def home(request):
    product_list = Product.objects.all()
    
    paginator = Paginator(product_list, 3) # Показывать 3 товара на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Skystore'
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    contact_info = {
        'country': 'Россия',
        'inn': '1234567890',
        'address': 'г. Москва, ул. Примерная, д. 1'
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')
    
    context = {
        'contact_info': contact_info
    }
    return render(request, 'catalog/contacts.html', context)

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'object': product,
        'title': f'Skystore - {product.name}'
    }
    return render(request, 'catalog/product_detail.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()
    context = {
        'form': form,
        'title': 'Добавить продукт'
    }
    return render(request, 'catalog/product_form.html', context)