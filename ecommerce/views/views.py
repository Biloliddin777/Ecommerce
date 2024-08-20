from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

from ecommerce.models import Customer
from ecommerce.forms import CustomerModelForm
from django.core.paginator import Paginator


# Create your views here.


def project_management(request):
    return render(request, 'ecommerce/project-management.html')


# def customers(request):
#     search_query = request.GET.get('search', '')
#     customers = Customer.objects.all()
#     paginator = Paginator(customers, 3)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     if search_query:
#         customers = customers.filter(
#             Q(first_name__icontains=search_query) |
#             Q(last_name__icontains=search_query) |
#             Q(email__icontains=search_query)
#         )
#
#     context = {
#         'customers': page_obj
#     }
#     return render(request, 'ecommerce/customers.html', context)

class CustomerModelFormView(View):
    def get(self, request):
        search_query = request.GET.get('search')
        customers = Customer.objects.all()
        paginator = Paginator(customers, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        if search_query:
            customers = customers.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        context = {
            'customers': page_obj
        }
        return render(request, 'ecommerce/customers.html', context)


# def customer_details(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     context = {'customer': customer}
#     return render(request, 'ecommerce/customer-details.html', context)


class CustomerDetailsView(View):
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        customer = get_object_or_404(Customer, id=customer_id)
        customer = Customer.objects.get(id=customer.id)
        context = {'customer': customer}
        return render(request, 'ecommerce/customer-details.html', context)


def profile(request):
    return render(request, 'ecommerce/profile.html')


def profile_settings(request):
    return render(request, 'ecommerce/settings.html')


# def add_customer(request):
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#     else:
#         form = CustomerModelForm()
#
#     context = {'form': form}
#     return render(request, 'ecommerce/add-customer.html', context)


class CustomerCreateView(View):
    def get(self, request):
        form = CustomerModelForm()
        return render(request, 'ecommerce/add-customer.html', {"form": form})

    def post(self, request):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')


# def edit_customer(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     form = CustomerModelForm(instance=customer)
#
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('ecommerce')
#     else:
#         form = CustomerModelForm(instance=customer)
#
#     context = {'form': form}
#     return render(request, 'ecommerce/edit-customer.html', context)


class CustomerUpdateView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerModelForm(instance=customer)
        return render(request, 'ecommerce/settings.html', {'form': form, 'customer': customer})

    def post(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

            return redirect("customer_details", customer_id)


# def delete_customer(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#
#     if request.method == "POST":
#         customer.delete()
#         return redirect('ecommerce')
#
#     return render(request, 'ecommerce/delete-customer.html', {'customer': customer})

class CustomerDeleteView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)

        if request.method == "POST":
            customer.delete()
            return redirect('ecommerce')

        return render(request, 'ecommerce/delete-customer.html', {'customer': customer})
