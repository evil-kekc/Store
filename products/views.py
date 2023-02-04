from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import ProductCategory, Product, Basket
from users.models import User


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
