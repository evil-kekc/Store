from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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


def products(request):
    """Products page display

    :param request: HttpRequest
    :return: object of products page
    """
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),

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
