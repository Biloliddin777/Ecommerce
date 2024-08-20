from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View

from product.models import Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from product.forms import ProductForm


# Create your views here.

# def product_list(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 3)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'products': page_obj
#     }
#     return render(request, 'product/product-list.html', context)

#
# class ProductListView(ListView):
#     def get(self, request):
#         products = Product.objects.all()
#         paginator = Paginator(products, 3)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         context = {
#             'products': page_obj
#         }
#         return render(request, 'product/product-list.html', context)


class ProductListView(ListView):
    def get(self, request, **kwargs):
        products = Product.objects.all()
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj
        }
        return render(request, 'product/product-list.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product-form.html'
    success_url = reverse_lazy('product-list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product-form.html'
    success_url = reverse_lazy('product-list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product-detail.html'
    context_object_name = 'product'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product-delete.html'
    success_url = reverse_lazy('product-list')
