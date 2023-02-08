from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from products.models import ProductCategory, Product, Basket


class IndexView(TemplateView):
    """Home page display"""
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        """Passing context

        :param kwargs:
        :return: context
        """
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        return context


class ProductsListView(ListView):
    """Products views"""
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self):
        """Filter products by category

        :return: Products filtered by category or all products
        """
        query_set = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return query_set.filter(category_id=category_id) if category_id else query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        """Passing context

        :param object_list: object_list of products.views.ProductsListView.get_context_data
        :param kwargs: kwargs of products.views.ProductsListView.get_context_data
        :return: context
        """
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context


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
