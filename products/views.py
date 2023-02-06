from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from products.models import ProductCategory, Product, Basket


def index(request):
    """Home page display

    :param request: HttpRequest
    :return: object HttpResponse of main page
    """
    context = {
        'title': 'Store',
    }
    return render(request=request, template_name='products/index.html', context=context)


def products(request, category_id=None, page_number=1):
    """Products page display

    :param page_number: Number of page
    :param category_id: product category id
    :param request: HttpRequest
    :return: object of products page
    """
    sorted_products = Product.objects.filter(category__id=category_id) if category_id else Product.objects.all()

    per_page = 3
    paginator = Paginator(sorted_products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator
    }
    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    """Add product at user basket

    :param request: HttpRequest
    :param product_id: ID of product
    :return: HttpResponseRedirect object of current page
    """
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.last()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    """Delete product by id

    :param request: HttpRequest
    :param basket_id: id id to be removed
    :return: HttpResponseRedirect object of current page
    """
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
